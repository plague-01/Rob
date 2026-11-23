#!/usr/bin/env python3
"""Soft-blob chibi cat ("Tofu"), in the rounded hand-drawn style:
head and body are one shape, ears grow out of the top corners, arms are
thin noodle strokes, feet are bumps on the bottom edge.

Writes:
  svg/tofu-cat.svg   layered character on the shared 400x500 canvas
  tofu-scene.svg     the character on a night stage (spotlight, skyline, railing, reflection)
Run: python3 cat.py
"""
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#1d1a1a"
FUR = "#e9a56b"      # ginger
FUR_DK = "#c97b3f"   # stripes / tail tip
PAW = "#fff1e0"
EAR_IN = "#f2a29b"


def o(fill, w=8):
    return f'fill="{fill}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'


def line(w=5, color=INK):
    return f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'


def L(name, content, pivot=None, hidden=False):
    piv = f' data-pivot="{pivot[0]} {pivot[1]}"' if pivot else ""
    hid = ' style="display:none"' if hidden else ""
    return (f'<g id="{name}" class="L-{name}" inkscape:groupmode="layer" '
            f'inkscape:label="{name}"{piv}{hid}>\n{content}\n</g>')


def noodle(d, fill, w=17):
    """Arm/tail drawn as a thick outlined stroke."""
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 14}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


# One blob for head + body; ear tips at the top corners, two foot bumps at the bottom.
BODY = ("M120,440 C104,440 98,428 101,408 C106,368 98,330 88,300 C76,268 62,240 68,206 "
        "C72,176 82,146 96,116 C114,138 130,154 152,160 C182,166 222,166 250,158 "
        "C272,152 288,136 304,114 C318,146 328,176 332,206 C338,240 324,268 312,300 "
        "C302,330 294,368 299,408 C302,428 296,440 280,440 "
        "L220,440 C215,428 207,423 200,423 C193,423 185,428 180,440 Z")

layers = [
    L("shadow", '<ellipse cx="200" cy="452" rx="125" ry="13" fill="#000" opacity=".14"/>'),
    L("tail", noodle("M292,410 C352,410 372,350 352,300 C342,276 360,258 376,270", FUR)
              + f'<path d="M352,300 C342,276 360,258 376,270" fill="none" stroke="{FUR_DK}" '
                f'stroke-width="17" stroke-linecap="round"/>', (292, 405)),
    L("body", "\n".join([
        L("body-base",
          f'<path d="{BODY}" {o(FUR)}/>'
          f'<g clip-path="url(#tofu-clip)">'
          # inner ears
          f'<path d="M100,134 C108,150 122,160 140,164 C122,158 108,148 100,134 Z" fill="{EAR_IN}" stroke="{EAR_IN}" stroke-width="14" stroke-linejoin="round"/>'
          f'<path d="M300,132 C292,148 278,158 260,162 C278,156 292,146 300,132 Z" fill="{EAR_IN}" stroke="{EAR_IN}" stroke-width="14" stroke-linejoin="round"/>'
          # cream paw tips + belly hint
          f'<ellipse cx="146" cy="446" rx="46" ry="20" fill="{PAW}"/>'
          f'<ellipse cx="254" cy="446" rx="46" ry="20" fill="{PAW}"/>'
          f'</g>'
          f'<path d="{BODY}" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
          f''),
        L("stripes", f'<path d="M186,172 l4,18 M200,170 v20 M214,172 l-4,18" {line(6, FUR_DK)}/>'),
        '<g transform="translate(0,46)">',
        L("brows", f'<circle cx="190" cy="176" r="3.5" fill="{INK}"/><path d="M220,170 l6,6" {line(5)}/>', (205, 174)),
        L("eyes", f'<circle cx="150" cy="214" r="14" fill="{INK}"/><circle cx="155" cy="208" r="4.5" fill="#fff"/>'
                  f'<circle cx="254" cy="210" r="14" fill="{INK}"/><circle cx="259" cy="204" r="4.5" fill="#fff"/>',
          (204, 212)),
        L("blush", '<ellipse cx="124" cy="246" rx="17" ry="9" fill="#f07f86" opacity=".45"/>'
                   '<ellipse cx="280" cy="242" rx="17" ry="9" fill="#f07f86" opacity=".45"/>'),
        L("whiskers", f'<path d="M108,234 l-22,-4 M110,248 l-22,4 M294,230 l22,-4 M292,244 l22,4" {line(4)}/>'),
        # open, happy mouth (default) and a closed ":3" swap for lip-sync / expressions
        L("mouth-open", f'<path d="M190,236 q-10,0 -14,-6 M190,236 q10,0 14,-6" {line(5)}/>'
                        f'<path d="M181,238 C182,262 200,266 202,244 Z" {o("#f2878f", 5)}/>'
                        f'<path d="M184,240 C186,254 196,256 199,246" fill="#ffb3b8"/>', (190, 245)),
        L("mouth-closed", f'<path d="M176,232 q7,9 14,0 q7,9 14,0" {line(5)}/>', (190, 236), hidden=True),
        "</g>",
    ]), (200, 440)),
    # left arm waves up, right hand rests on the hip
    L("arm-left", noodle("M104,334 C74,322 54,296 50,262", FUR), (104, 334)),
    L("arm-right", noodle("M298,330 C334,344 334,378 306,390", FUR), (298, 330)),
]

CHAR = "\n".join(layers)
DEFS = f'<clipPath id="tofu-clip"><path d="{BODY}"/></clipPath>'
HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
        'xmlns:xlink="http://www.w3.org/1999/xlink"')

os.makedirs(os.path.join(HERE, "svg"), exist_ok=True)
with open(os.path.join(HERE, "svg", "tofu-cat.svg"), "w") as f:
    f.write(f'{HEAD} viewBox="0 0 400 500" width="400" height="500" data-character="tofu">\n'
            f'<title>Tofu (cat)</title>\n<defs>{DEFS}</defs>\n{CHAR}\n</svg>\n')

# ---------------- scene -------------------------------------------------------
W, H = 720, 1120
rnd = random.Random(7)
stars = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, 560):.0f}" '
                f'r="{rnd.choice([1, 1, 1.4, 2])}" fill="#fff" opacity="{rnd.uniform(.4, .95):.2f}"/>'
                for _ in range(140))


def skyline():
    s, x = "", -10
    while x < W:
        w = rnd.randint(40, 90)
        h = rnd.randint(30, 110) if not (220 < x < 500) else rnd.randint(10, 40)
        top = 660 - h
        s += f'<rect x="{x}" y="{top}" width="{w}" height="{h + 20}" fill="#1c1418"/>'
        for wy in range(top + 8, 650, 14):
            for wx in range(x + 6, x + w - 10, 14):
                if rnd.random() < .3:
                    s += f'<rect x="{wx}" y="{wy}" width="7" height="4" fill="#ffd9a8" opacity=".6"/>'
        x += w + rnd.randint(0, 30)
    return s


rail = '<rect x="0" y="738" width="720" height="8" fill="#1c1418"/>'
rail += "".join(f'<rect x="{x}" y="738" width="7" height="58" fill="#1c1418"/>' for x in range(20, 720, 74))

scene = f'''{HEAD} viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<title>Tofu on stage</title>
<defs>
{DEFS}
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#161018"/><stop offset=".55" stop-color="#3b2232"/><stop offset="1" stop-color="#b0566f"/>
</linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#6a4a5e"/><stop offset="1" stop-color="#1c1219"/>
</linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#ffe7c2" stop-opacity=".05"/><stop offset="1" stop-color="#ffe7c2" stop-opacity=".22"/>
</linearGradient>
<filter id="shade"><feColorMatrix type="matrix" values="0 0 0 0 .1  0 0 0 0 .06  0 0 0 0 .09  0 0 0 1 0"/><feGaussianBlur stdDeviation="3"/></filter>
<g id="tofu">{CHAR}</g>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
{stars}
<rect x="0" y="640" width="{W}" height="110" fill="#c3627c" opacity=".55"/>
{skyline()}
{rail}
<rect x="0" y="796" width="{W}" height="{H - 796}" fill="url(#floor)"/>
<path d="M270,0 L450,0 L620,860 L100,860 Z" fill="url(#beam)"/>
<g transform="translate(140,1298) scale(1.1,-1.1)" filter="url(#shade)" opacity=".45"><use href="#tofu"/></g>
<g transform="translate(140,330) scale(1.1)"><use href="#tofu"/></g>
</svg>
'''
with open(os.path.join(HERE, "tofu-scene.svg"), "w") as f:
    f.write(scene)
print("wrote svg/tofu-cat.svg and tofu-scene.svg")
