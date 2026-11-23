#!/usr/bin/env python3
"""Four sitting kawaii cats that share one pose and differ by coat pattern.

Writes svg/cat-<name>.svg (layered, 400x480 canvas) and sitting-cats.svg (2x2 sheet).
Run: python3 sitting_cats.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#2a2523"
HEAD_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"')


def line(w=5, color=INK):
    return f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'


def L(name, content, pivot=None):
    piv = f' data-pivot="{pivot[0]} {pivot[1]}"' if pivot else ""
    return (f'<g id="{name}" class="L-{name}" inkscape:groupmode="layer" '
            f'inkscape:label="{name}"{piv}>\n{content}\n</g>')


# ---- shared geometry -------------------------------------------------------
HEAD = ("M100,215 C92,170 100,130 118,108 L112,48 C140,58 162,74 176,92 "
        "C192,89 208,89 224,92 C238,74 260,58 288,48 L282,108 "
        "C300,130 308,170 300,215 C292,262 250,282 200,282 C150,282 108,262 100,215 Z")
BODY = ("M142,250 C120,300 104,362 110,410 C113,430 130,437 150,437 L272,437 "
        "C302,437 318,420 312,394 C306,350 286,292 262,250 Z")
TAIL = "M282,414 C352,420 368,344 342,284 C334,264 348,248 364,258"
def leg(x):
    """Front leg: rounded paw at the bottom; the outline is left open at the top so it blends into the chest."""
    open_d = f"M{x},320 V420 C{x},434 {x+6},439 {x+20},439 C{x+34},439 {x+40},434 {x+40},420 V320"
    return open_d + " Z", open_d


LEGS = {"left": leg(150), "right": leg(206)}
EAR_IN_L = "M124,102 L120,66 C136,74 148,84 158,95 Z"
EAR_IN_R = "M276,102 L280,66 C264,74 252,84 242,95 Z"


def part(key, name, d, base, patches="", w=7, outline=None):
    """Fill a shape, paint pattern patches clipped inside it, then outline it."""
    cid = f"{key}-{name}-clip"
    return (f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
            f'<path d="{d}" fill="{base}"/>'
            f'<g clip-path="url(#{cid})">{patches}</g>'
            f'<path d="{outline or d}" fill="none" stroke="{INK}" stroke-width="{w}" '
            f'stroke-linejoin="round" stroke-linecap="round"/>')


def tail(key, base, patches=""):
    cid = f"{key}-tail-clip"
    # The clip is the stroke's footprint, drawn as a fat stroke inside a mask.
    return (f'<mask id="{cid}" maskUnits="userSpaceOnUse" x="0" y="0" width="400" height="480">'
            f'<path d="{TAIL}" fill="none" stroke="#fff" stroke-width="30" stroke-linecap="round"/></mask>'
            f'<path d="{TAIL}" fill="none" stroke="{INK}" stroke-width="44" stroke-linecap="round"/>'
            f'<path d="{TAIL}" fill="none" stroke="{base}" stroke-width="30" stroke-linecap="round"/>'
            f'<g mask="url(#{cid})">{patches}</g>')


def stripes(xys, color, w=9):
    return "".join(f'<path d="{d}" {line(w, color)}/>' for d in xys)


def cat(key, title, c):
    eye = c.get("eye", INK)
    face = [
        L("eyes", f'<ellipse cx="160" cy="200" rx="11" ry="13" fill="{eye}"/>'
                  f'<ellipse cx="240" cy="200" rx="11" ry="13" fill="{eye}"/>'
                  f'<circle cx="164" cy="195" r="4" fill="#fff"/><circle cx="244" cy="195" r="4" fill="#fff"/>',
          (200, 200)),
        L("blush", '<ellipse cx="134" cy="228" rx="14" ry="7" fill="#f3a0a8" opacity=".5"/>'
                   '<ellipse cx="266" cy="228" rx="14" ry="7" fill="#f3a0a8" opacity=".5"/>'),
        L("nose", f'<path d="M194,214 h12 l-6,6 Z" fill="{c.get("nose", "#e88f9a")}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>',
          (200, 216)),
        L("mouth", f'<path d="M186,224 q7,8 14,0 q7,8 14,0" {line(4.5)}/>', (200, 226)),
        L("whiskers", f'<path d="M104,210 l-30,-5 M104,222 l-30,4 M296,210 l30,-5 M296,222 l30,4" {line(3.5)}/>'),
    ]
    layers = [
        L("shadow", '<ellipse cx="215" cy="446" rx="130" ry="12" fill="#000" opacity=".12"/>'),
        L("tail", tail(key, c["tail"], c.get("tail_p", "")), (282, 414)),
        L("body", part(key, "body", BODY, c["body"], c.get("body_p", ""))
                  + f'<path d="M262,437 C256,398 276,372 304,380" {line(6)}/>', (210, 437)),
        L("leg-left", part(key, "legl", LEGS["left"][0], c["legs"], c.get("legl_p", ""), w=6, outline=LEGS["left"][1])
                      + f'<path d="M163,438 v-11 M177,438 v-11" {line(3.5)}/>', (170, 330)),
        L("leg-right", part(key, "legr", LEGS["right"][0], c["legs"], c.get("legr_p", ""), w=6, outline=LEGS["right"][1])
                       + f'<path d="M219,438 v-11 M233,438 v-11" {line(3.5)}/>', (226, 330)),
        L("head", part(key, "head", HEAD, c["head"],
                       c.get("head_p", "")
                       + f'<path d="{EAR_IN_L}" fill="{c.get("ear_in", "#f5b8bf")}"/>'
                       + f'<path d="{EAR_IN_R}" fill="{c.get("ear_in", "#f5b8bf")}"/>')
                  + "\n" + "\n".join(face), (200, 280)),
    ]
    return "\n".join(layers)


# ---- coat patterns ---------------------------------------------------------
WHITE = "#fffaf3"
CATS = {
    "maple": ("Maple (ginger tabby)", dict(
        head="#f2a75f", body="#f2a75f", legs=WHITE, tail="#f2a75f",
        head_p=(f'<path d="M150,282 C150,236 176,212 200,204 C224,212 250,236 250,282 Z" fill="{WHITE}"/>'
                + stripes(["M186,100 l3,22", "M200,96 v24", "M214,100 l-3,22",
                           "M104,170 l22,6", "M296,170 l-22,6"], "#c97a35")),
        body_p=(f'<ellipse cx="200" cy="330" rx="52" ry="70" fill="{WHITE}"/>'
                + stripes(["M282,300 l-20,8", "M294,334 l-22,6"], "#c97a35")),
        tail_p=stripes(["M318,404 l-8,-22", "M350,360 l-24,-4", "M350,310 l-24,2"], "#c97a35", 10),
    )),
    "pepper": ("Pepper (gray tuxedo tabby)", dict(
        head="#5c5d66", body="#5c5d66", legs=WHITE, tail="#5c5d66", ear_in="#f2a9b3",
        head_p=(f'<path d="M96,282 L96,236 C140,232 172,226 188,192 L200,168 L212,192 '
                f'C228,226 260,232 304,236 L304,282 Z" fill="{WHITE}"/>'
                + stripes(["M184,104 l3,24", "M200,98 v28", "M216,104 l-3,24",
                           "M104,176 l24,8", "M296,176 l-24,8"], "#3c3d44")),
        body_p=(f'<path d="M150,262 C170,300 176,330 200,360 C224,330 230,300 250,262 Z" fill="{WHITE}"/>'
                + stripes(["M284,296 l-22,8", "M296,330 l-24,6", "M300,364 l-24,4"], "#3c3d44")),
        tail_p=stripes(["M316,404 l-8,-22", "M348,362 l-26,-4", "M350,312 l-26,2"], "#3c3d44", 10),
    )),
    "patch": ("Patch (calico)", dict(
        head=WHITE, body=WHITE, legs=WHITE, tail="#f0a35e",
        head_p=('<path d="M90,40 L190,40 C186,92 160,128 120,150 C104,158 92,150 90,140 Z" fill="#f0a35e"/>'
                '<path d="M226,40 L310,40 L310,170 C282,168 250,140 236,110 C230,94 226,70 226,40 Z" fill="#45403f"/>'),
        body_p=('<path d="M262,250 C240,280 236,320 262,350 C286,372 312,360 320,340 L320,250 Z" fill="#45403f"/>'
                '<ellipse cx="128" cy="392" rx="30" ry="22" fill="#f0a35e"/>'),
        tail_p='<circle cx="364" cy="258" r="34" fill="#45403f"/>',
        legr_p='<rect x="200" y="404" width="52" height="40" fill="#f0a35e"/>',
    )),
    "lilac": ("Lilac (soft gray)", dict(
        head="#c9c3d4", body="#c9c3d4", legs="#f6f2fa", tail="#c9c3d4", ear_in="#f6c1cc",
        head_p=(f'<ellipse cx="200" cy="252" rx="62" ry="36" fill="#f6f2fa"/>'
                + stripes(["M188,100 l2,18", "M200,96 v20", "M212,100 l-2,18"], "#a69eb4", 7)),
        body_p='<ellipse cx="200" cy="330" rx="50" ry="68" fill="#f6f2fa"/>',
        tail_p='<circle cx="364" cy="258" r="40" fill="#a69eb4"/>',
    )),
}

os.makedirs(os.path.join(HERE, "svg"), exist_ok=True)
built = {}
for key, (title, c) in CATS.items():
    content = cat(key, title, c)
    built[key] = content
    with open(os.path.join(HERE, "svg", f"cat-{key}.svg"), "w") as f:
        f.write(f'{HEAD_SVG} viewBox="0 0 400 480" width="400" height="480" data-character="{key}">\n'
                f'<title>{title}</title>\n{content}\n</svg>\n')

# 2x2 sheet
cells = ""
for i, key in enumerate(CATS):
    x, y = (i % 2) * 400, (i // 2) * 500
    inner = built[key].replace(' id="', f' id="{key}-sheet-')
    # clip/mask ids were renamed by the line above; point references at the new ids
    inner = inner.replace(f'url(#{key}-', f'url(#{key}-sheet-{key}-')
    name = CATS[key][0]
    cells += (f'<g transform="translate({x},{y})">{inner}'
              f'<text x="200" y="488" text-anchor="middle" font-family="system-ui, sans-serif" '
              f'font-size="20" font-weight="600" fill="#4a4340">{name}</text></g>')
with open(os.path.join(HERE, "sitting-cats.svg"), "w") as f:
    f.write(f'{HEAD_SVG} viewBox="0 0 800 1000" width="800" height="1000">\n<title>Sitting cats</title>\n'
            f'<rect width="800" height="1000" fill="#eceae6"/>\n{cells}\n</svg>\n')
print("wrote", ", ".join(f"svg/cat-{k}.svg" for k in CATS), "and sitting-cats.svg")
