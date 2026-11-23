#!/usr/bin/env python3
"""Soft-blob chibi bear couple: Honey (female) and Cocoa (male).

Writes:
  svg/honey-bear.svg, svg/cocoa-bear.svg   layered characters, shared 400x500 canvas
  bears-scene.svg                          both bears on the night stage
Run: python3 bears.py
"""
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#1d1a1a"
PAW = "#fff1e0"
HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
        'xmlns:xlink="http://www.w3.org/1999/xlink"')


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
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 14}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


# Head + body blob with flared top corners and two foot bumps.
BODY = ("M120,440 C104,440 98,428 101,408 C106,368 98,330 88,300 C76,268 60,240 66,200 "
        "C70,170 80,150 102,144 C140,138 170,146 200,146 C230,146 262,138 298,144 "
        "C320,150 330,170 334,200 C340,240 324,268 312,300 C302,330 294,368 299,408 "
        "C302,428 296,440 280,440 L220,440 C215,428 207,423 200,423 C193,423 185,428 180,440 Z")

ARMS = {
    "left-up": "M104,334 C74,322 54,296 50,262",
    "left-hip": "M102,330 C66,344 66,378 94,390",
    "right-up": "M296,334 C326,322 346,296 350,262",
    "right-hip": "M298,330 C334,344 334,378 306,390",
}


def bear(key, fur, ear_in, muzzle, female, wave_side):
    eyes = (f'<circle cx="150" cy="258" r="14" fill="{INK}"/><circle cx="155" cy="252" r="4.5" fill="#fff"/>'
            f'<circle cx="250" cy="258" r="14" fill="{INK}"/><circle cx="255" cy="252" r="4.5" fill="#fff"/>')
    if female:
        eyes += f'<path d="M137,248 l-10,-6 M138,256 l-11,-1 M263,248 l10,-6 M262,256 l11,-1" {line(4)}/>'
        mouth_default = L("mouth-closed", f'<path d="M186,292 q7,9 14,0 q7,9 14,0" {line(5)}/>', (200, 294))
        mouth_alt = L("mouth-open", f'<path d="M186,292 q7,6 14,0 q7,6 14,0" {line(5)}/>'
                                    f'<path d="M190,296 C190,318 210,318 210,296 Z" {o("#f2878f", 5)}/>',
                      (200, 300), hidden=True)
        extra = L("bow", f'<g transform="rotate(18 292 132)">'
                         f'<path d="M292,132 L262,114 L262,150 Z" {o("#f58fae", 6)}/>'
                         f'<path d="M292,132 L322,114 L322,150 Z" {o("#f58fae", 6)}/>'
                         f'<circle cx="292" cy="132" r="9" {o("#f9b3c8", 5)}/></g>', (292, 132))
        brows = ""
    else:
        mouth_default = L("mouth-open", f'<path d="M186,292 q7,6 14,0 q7,6 14,0" {line(5)}/>'
                                        f'<path d="M188,296 C186,326 214,326 212,296 Z" {o("#f2878f", 5)}/>'
                                        f'<path d="M192,304 C194,318 206,318 208,304" fill="#ffb3b8"/>', (200, 304))
        mouth_alt = L("mouth-closed", f'<path d="M186,292 q7,9 14,0 q7,9 14,0" {line(5)}/>', (200, 294), hidden=True)
        extra = L("tuft", f'<path d="M184,148 C182,126 192,118 198,112 C198,126 204,132 212,128 C210,138 206,144 204,148" {o(fur, 6)}/>',
                  (198, 146))
        brows = L("brows", f'<circle cx="186" cy="222" r="3.5" fill="{INK}"/><path d="M212,216 l7,6" {line(5)}/>', (200, 220))

    arm_l = ARMS["left-up"] if wave_side == "left" else ARMS["left-hip"]
    arm_r = ARMS["right-up"] if wave_side == "right" else ARMS["right-hip"]
    body_inner = [
        L("body-base",
          f'<path d="{BODY}" {o(fur)}/>'
          f'<g clip-path="url(#{key}-clip)">'
          f'<ellipse cx="146" cy="446" rx="46" ry="20" fill="{PAW}"/>'
          f'<ellipse cx="254" cy="446" rx="46" ry="20" fill="{PAW}"/></g>'
          f'<path d="{BODY}" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'),
        L("muzzle", f'<ellipse cx="200" cy="290" rx="40" ry="27" fill="{muzzle}"/>'),
    ]
    if brows:
        body_inner.append(brows)
    body_inner += [
        L("eyes", eyes, (200, 258)),
        L("blush", '<ellipse cx="118" cy="292" rx="17" ry="9" fill="#f07f86" opacity=".45"/>'
                   '<ellipse cx="282" cy="292" rx="17" ry="9" fill="#f07f86" opacity=".45"/>'),
        L("nose", f'<ellipse cx="200" cy="278" rx="10" ry="7" fill="{INK}"/>'
                  f'<ellipse cx="197" cy="276" rx="3" ry="2" fill="#fff" opacity=".7"/>', (200, 278)),
        mouth_default,
        mouth_alt,
    ]
    ear = lambda cx, ix: (f'<circle cx="{cx}" cy="140" r="34" {o(fur)}/>'
                          f'<circle cx="{ix}" cy="136" r="16" fill="{ear_in}"/>')
    layers = [
        L("shadow", '<ellipse cx="200" cy="452" rx="125" ry="13" fill="#000" opacity=".14"/>'),
        L("ear-left", ear(108, 112), (112, 160)),
        L("ear-right", ear(292, 288), (288, 160)),
    ]
    if not female:
        layers.append(extra)  # tuft sits behind the head outline
    layers += [
        L("body", "\n".join(body_inner), (200, 440)),
        L("arm-left", noodle(arm_l, fur), (104, 332)),
        L("arm-right", noodle(arm_r, fur), (296, 332)),
    ]
    if female:
        layers.append(extra)  # bow sits on top of the ear
    return "\n".join(layers), f'<clipPath id="{key}-clip"><path d="{BODY}"/></clipPath>'


BEARS = {
    "honey": dict(title="Honey (bear, female)", fur="#d9a77f", ear_in="#f4c9b0", muzzle="#f3d3b5",
                  female=True, wave_side="left"),
    "cocoa": dict(title="Cocoa (bear, male)", fur="#a8693f", ear_in="#d9a07a", muzzle="#d6a27a",
                  female=False, wave_side="right"),
}

os.makedirs(os.path.join(HERE, "svg"), exist_ok=True)
built = {}
for key, b in BEARS.items():
    content, clip = bear(key, b["fur"], b["ear_in"], b["muzzle"], b["female"], b["wave_side"])
    built[key] = (content, clip)
    with open(os.path.join(HERE, "svg", f"{key}-bear.svg"), "w") as f:
        f.write(f'{HEAD} viewBox="0 0 400 500" width="400" height="500" data-character="{key}">\n'
                f'<title>{b["title"]}</title>\n<defs>{clip}</defs>\n{content}\n</svg>\n')

# ---------------- scene -------------------------------------------------------
W, H, FLOOR = 720, 1120, 814
rnd = random.Random(11)
stars = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, 600):.0f}" '
                f'r="{rnd.choice([1, 1, 1.4, 2])}" fill="#fff" opacity="{rnd.uniform(.4, .95):.2f}"/>'
                for _ in range(150))
city, x = "", -10
while x < W:
    w = rnd.randint(40, 90)
    h = rnd.randint(30, 110) if not (240 < x < 470) else rnd.randint(20, 60)
    top = 660 - h
    city += f'<rect x="{x}" y="{top}" width="{w}" height="{h + 20}" fill="#1c1418"/>'
    for wy in range(top + 8, 650, 14):
        for wx in range(x + 6, x + w - 10, 14):
            if rnd.random() < .3:
                city += f'<rect x="{wx}" y="{wy}" width="7" height="4" fill="#ffd9a8" opacity=".6"/>'
    x += w + rnd.randint(0, 30)
rail = '<rect x="0" y="738" width="720" height="8" fill="#1c1418"/>'
rail += "".join(f'<rect x="{x}" y="738" width="7" height="58" fill="#1c1418"/>' for x in range(20, 720, 74))

S = 0.92
TY = FLOOR - 440 * S
placed, defs = "", ""
for key, tx in (("honey", -10), ("cocoa", 330)):
    content, clip = built[key]
    content = content.replace(' id="', f' id="{key}-')  # keep ids unique inside one file
    defs += clip + f'<g id="{key}">{content}</g>'
    placed += (f'<g transform="translate({tx},{2 * FLOOR - TY:.1f}) scale({S},{-S})" filter="url(#shade)" opacity=".45">'
               f'<use href="#{key}"/></g>')
    placed += f'<g transform="translate({tx},{TY:.1f}) scale({S})"><use href="#{key}"/></g>'

scene = f'''{HEAD} viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<title>Honey and Cocoa on stage</title>
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#161018"/><stop offset=".55" stop-color="#3b2232"/><stop offset="1" stop-color="#b0566f"/>
</linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#6a4a5e"/><stop offset="1" stop-color="#1c1219"/>
</linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#ffe7c2" stop-opacity=".05"/><stop offset="1" stop-color="#ffe7c2" stop-opacity=".2"/>
</linearGradient>
<filter id="shade"><feColorMatrix type="matrix" values="0 0 0 0 .1  0 0 0 0 .06  0 0 0 0 .09  0 0 0 1 0"/><feGaussianBlur stdDeviation="3"/></filter>
{defs}
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
{stars}
<rect x="0" y="640" width="{W}" height="110" fill="#c3627c" opacity=".55"/>
{city}
{rail}
<rect x="0" y="796" width="{W}" height="{H - 796}" fill="url(#floor)"/>
<path d="M250,0 L470,0 L660,860 L60,860 Z" fill="url(#beam)"/>
{placed}
</svg>
'''
with open(os.path.join(HERE, "bears-scene.svg"), "w") as f:
    f.write(scene)
print("wrote svg/honey-bear.svg, svg/cocoa-bear.svg, bears-scene.svg")
