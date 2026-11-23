#!/usr/bin/env python3
"""Generate layered, animation-ready chibi character SVGs.

Every character is drawn on the same 400x500 canvas (ground line y=462),
so they line up when placed side by side. Each moving part is its own
Inkscape-compatible layer (<g inkscape:groupmode="layer">) with a
data-pivot="x y" attribute marking its rotation/scale origin.

Run:  python3 build.py   -> writes svg/*.svg and preview.html
"""
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "svg")
INK = "#1d1a1a"
SKIN = "#fdfcf8"


# ---------- helpers ----------------------------------------------------------
def o(fill, w=7):
    """Fill plus the thick black outline used across the style."""
    return (f'fill="{fill}" stroke="{INK}" stroke-width="{w}" '
            f'stroke-linejoin="round" stroke-linecap="round"')


def line(w=5, color=INK):
    return f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'


def L(name, content, pivot=None):
    piv = f' data-pivot="{pivot[0]} {pivot[1]}"' if pivot else ""
    return (f'<g id="{name}" class="L-{name}" inkscape:groupmode="layer" '
            f'inkscape:label="{name}"{piv}>\n{content}\n</g>')


def svg(key, title, layers, defs=""):
    body = "\n".join(layers)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" viewBox="0 0 400 500" width="400" height="500" data-character="{key}">
<title>{title}</title>
<defs>{defs}</defs>
{body}
</svg>
'''


def shadow(rx=110, cy=462):
    return L("shadow", f'<ellipse cx="200" cy="{cy}" rx="{rx}" ry="14" fill="#000" opacity=".14"/>')


def eyes(cy, dx=42, rx=10, ry=17, cx=200, lashes=False):
    s = ""
    for x in (cx - dx, cx + dx):
        s += f'<ellipse cx="{x}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{INK}"/>'
        s += f'<circle cx="{x + rx * .3:.1f}" cy="{cy - ry * .4:.1f}" r="{max(2.5, rx * .32):.1f}" fill="#fff"/>'
    if lashes:
        s += f'<path d="M{cx-dx-rx+1},{cy-8} l-9,-3 M{cx+dx+rx-1},{cy-8} l9,-3" {line(4)}/>'
    return L("eyes", s, (cx, cy))


def blush(cy, dx=72, color="#f59aa6"):
    return L("blush", f'<ellipse cx="{200-dx}" cy="{cy}" rx="17" ry="9" fill="{color}" opacity=".55"/>'
                      f'<ellipse cx="{200+dx}" cy="{cy}" rx="17" ry="9" fill="{color}" opacity=".55"/>')


# Shared blob body for animal / monster characters (head + body in one shape)
BLOB = ("M100,150 C95,95 130,85 200,85 C270,85 305,95 300,150 C302,230 305,330 312,400 "
        "C315,425 300,437 270,437 L130,437 C100,437 85,425 88,400 C95,330 98,230 100,150 Z")


def blob_feet(color):
    return [L("leg-left", f'<rect x="138" y="400" width="50" height="54" rx="18" {o(color)}/>', (163, 410)),
            L("leg-right", f'<rect x="212" y="400" width="50" height="54" rx="18" {o(color)}/>', (237, 410))]


def blob_arm(side, color, angle=None, extra=""):
    if side == "left":
        px, py, a = 104, 285, 28 if angle is None else angle
    else:
        px, py, a = 296, 285, -28 if angle is None else angle
    name = "arm-left" if side == "left" else "arm-right"
    g = (f'<g transform="rotate({a} {px} {py})">'
         f'<rect x="{px-19}" y="{py-10}" width="38" height="62" rx="19" {o(color)}/>{extra}</g>')
    return L(name, g, (px, py))


# Shared human parts ------------------------------------------------------------
HEAD = dict(x=82, y=50, w=236, h=205, rx=72)


def human_legs(color):
    return [L("leg-left", f'<rect x="148" y="330" width="48" height="122" rx="14" {o(color)}/>'
                          f'<path d="M154,430 h36" {line(4)} opacity=".35"/>', (172, 340)),
            L("leg-right", f'<rect x="204" y="330" width="48" height="122" rx="14" {o(color)}/>'
                           f'<path d="M210,430 h36" {line(4)} opacity=".35"/>', (228, 340))]


def human_arm(side, sleeve, angle=None, hand=SKIN):
    if side == "left":
        px, py, a = 144, 282, 22 if angle is None else angle
    else:
        px, py, a = 256, 282, -22 if angle is None else angle
    name = "arm-left" if side == "left" else "arm-right"
    g = (f'<g transform="rotate({a} {px} {py})">'
         f'<rect x="{px-20}" y="{py-14}" width="40" height="66" rx="18" {o(sleeve)}/>'
         f'<circle cx="{px}" cy="{py+62}" r="23" {o(hand)}/></g>')
    return L(name, g, (px, py))


def torso(color, extra=""):
    p = "M140,262 L260,262 C268,300 272,335 270,370 L130,370 C128,335 132,300 140,262 Z"
    return L("torso", f'<path d="{p}" {o(color)}/>{extra}', (200, 360))


def human_head(key, hair_back, hair_front, face, skin=SKIN):
    h = HEAD
    rect = f'x="{h["x"]}" y="{h["y"]}" width="{h["w"]}" height="{h["h"]}" rx="{h["rx"]}"'
    hair_path = re.search(r'd="([^"]+)"', hair_front).group(1)
    base = (f'<rect {rect} {o(skin)}/>'
            # soft shading cast by the hair onto the face
            f'<g clip-path="url(#{key}-clip)"><path d="{hair_path}" transform="translate(0,14)" '
            f'fill="#000" opacity=".08"/></g>')
    parts = []
    if hair_back:
        parts.append(L("hair-back", hair_back, (200, 120)))
    parts.append(L("face-base", base))
    parts.extend(face)
    parts.append(L("hair-front", hair_front, (200, 80)))
    defs = f'<clipPath id="{key}-clip"><rect {rect}/></clipPath>'
    return L("head", "\n".join(parts), (200, 250)), defs


# ---------- characters --------------------------------------------------------
chars = {}

# 1. MILO - human boy, messy hair, orange hoodie
hair = ("M74,175 C62,92 108,36 200,34 C292,36 338,92 326,175 L310,160 L304,128 L284,146 L266,112 "
        "L246,138 L226,106 L204,134 L184,104 L164,136 L144,108 L126,146 L108,124 L98,165 Z")
hair_front = (f'<path d="M188,40 C174,12 200,0 220,12 C210,18 205,28 206,40 Z" {o("#2d2f45")}/>'
              f'<path d="{hair}" {o("#2d2f45")}/>'
              f'<path d="M150,62 q-12,20 -8,42 M252,62 q12,22 6,42 M200,48 q-6,18 -2,36" {line(4, "#55597a")}/>')
head, defs = human_head("milo", None, hair_front, [
    eyes(178),
    L("brows", f'<path d="M150,150 l14,-4 M236,146 l14,4" {line(4)}/>'),
    blush(212),
    L("mouth", f'<ellipse cx="200" cy="216" rx="6" ry="6" {o("#6b2f2f", 4)}/>', (200, 216)),
])
hoodie_extra = (f'<path d="M146,268 C170,292 230,292 254,268" {line(5)}/>'
                f'<path d="M186,284 v28 M214,284 v28" {line(4)}/>'
                f'<circle cx="186" cy="316" r="4" fill="{INK}"/><circle cx="214" cy="316" r="4" fill="{INK}"/>'
                f'<path d="M160,365 L168,334 L232,334 L240,365" {line(4)}/>')
chars["milo"] = ("Milo (human)", [
    shadow(),
    *human_legs("#3f6f5e"),
    human_arm("left", "#f08a3c"),
    torso("#f08a3c", hoodie_extra),
    head,
    human_arm("right", "#f08a3c"),
], defs)

# 2. JUNO - human girl, twin buns, teal raincoat, star clip
hair_back = (f'<circle cx="112" cy="72" r="40" {o("#e0a33a")}/>'
             f'<circle cx="288" cy="72" r="40" {o("#e0a33a")}/>'
             f'<rect x="66" y="74" width="268" height="168" rx="60" {o("#e0a33a")}/>'
             f'<path d="M100,60 q10,-14 24,-10 M276,50 q14,-4 24,10" {line(4, "#b07a1f")}/>')
jhair = ("M78,204 C66,98 112,42 200,42 C288,42 334,98 322,204 L302,204 L300,134 "
         "C262,132 236,122 220,102 C200,126 150,136 100,134 L98,204 Z")
hair_front = (f'<path d="{jhair}" {o("#e0a33a")}/>'
              f'<path d="M160,64 q-8,30 -26,60 M232,70 q22,22 52,40" {line(4, "#b07a1f")}/>'
              f'<path d="M282,96 l6,14 15,1 -11,10 4,15 -14,-8 -13,8 4,-15 -11,-10 15,-1 Z" {o("#ffd84a", 4)}/>')
head, defs = human_head("juno", hair_back, hair_front, [
    eyes(182, lashes=True),
    blush(214),
    L("mouth", f'<path d="M190,218 q10,9 20,0" {line(5)}/>', (200, 218)),
])
coat_extra = (f'<path d="M200,272 L200,368" {line(4)}/>'
              f'<circle cx="212" cy="300" r="5" fill="{INK}"/><circle cx="212" cy="336" r="5" fill="{INK}"/>'
              f'<path d="M148,262 L196,262 L178,294 Z" {o("#7fd1c9", 5)}/>'
              f'<path d="M252,262 L204,262 L222,294 Z" {o("#7fd1c9", 5)}/>')
chars["juno"] = ("Juno (human)", [
    shadow(),
    *human_legs("#e0705e"),
    human_arm("left", "#3fa7a0"),
    torso("#3fa7a0", coat_extra),
    head,
    human_arm("right", "#3fa7a0"),
], defs)

# 3. PIP - fox kit
FOX = "#e98a43"
CREAM = "#fff1de"
fox_body = (f'<path d="{BLOB}" {o(FOX)}/>'
            f'<g clip-path="url(#pip-clip)">'
            f'<ellipse cx="200" cy="385" rx="78" ry="70" fill="{CREAM}" stroke="{INK}" stroke-width="5"/>'
            f'<ellipse cx="146" cy="246" rx="56" ry="34" fill="{CREAM}"/>'
            f'<ellipse cx="254" cy="246" rx="56" ry="34" fill="{CREAM}"/></g>'
            f'<path d="{BLOB}" fill="none" stroke="{INK}" stroke-width="7"/>')
chars["pip"] = ("Pip (fox)", [
    shadow(),
    L("tail", f'<path d="M285,395 C360,400 395,320 370,240 C355,295 330,330 292,338 Z" {o(FOX)}/>'
              f'<path d="M370,240 C380,270 378,300 368,322 C356,300 360,268 370,240 Z" {o(CREAM, 5)}/>',
      (292, 380)),
    L("ear-left", f'<path d="M112,150 L118,48 L190,96 Z" {o(FOX)}/><path d="M130,118 L132,78 L164,100 Z" fill="#7a3d1c"/>', (150, 110)),
    L("ear-right", f'<path d="M288,150 L282,48 L210,96 Z" {o(FOX)}/><path d="M270,118 L268,78 L236,100 Z" fill="#7a3d1c"/>', (250, 110)),
    *blob_feet("#5b3424"),
    blob_arm("left", FOX),
    L("body", "\n".join([
        L("body-base", fox_body),
        L("marks", f'<path d="M188,140 l-3,8 M212,140 l3,8" {line(4)}/>'),
        eyes(206, dx=48, rx=11, ry=13),
        blush(238, dx=80),
        L("mouth", f'<path d="M193,226 q7,-5 14,0 q-7,8 -14,0 Z" fill="{INK}"/>'
                   f'<path d="M186,240 q7,8 14,0 q7,8 14,0" {line(4)}/>', (200, 235)),
    ]), (200, 437)),
    blob_arm("right", FOX),
], f'<clipPath id="pip-clip"><path d="{BLOB}"/></clipPath>')

# 4. LUMI - lamb (cloud of wool)
WOOL = "#fbf7ef"
pts = []
for i in range(9):
    pts.append((112 + i * 22, 102))       # top edge
    pts.append((112 + i * 22, 418))       # bottom edge
for j in range(1, 14):
    pts.append((100, 102 + j * 23))       # left edge
    pts.append((300, 102 + j * 23))       # right edge
pts = sorted(set(pts))
wool = "".join(f'<circle cx="{x}" cy="{y}" r="26" {o(WOOL)}/>' for x, y in pts)
wool += "".join(f'<circle cx="{x}" cy="{y}" r="22.5" fill="{WOOL}"/>' for x, y in pts)
wool += f'<rect x="100" y="102" width="200" height="316" fill="{WOOL}"/>'
wool += f'<path d="M150,330 q14,-12 28,0 M220,360 q14,-12 28,0 M140,390 q12,-10 24,0" {line(4, "#d9d0bf")}/>'
chars["lumi"] = ("Lumi (lamb)", [
    shadow(),
    *blob_feet("#5a4033"),
    L("arm-left", f'<g transform="rotate(28 106 288)"><circle cx="106" cy="320" r="26" {o(WOOL)}/>'
                  f'<rect x="94" y="336" width="24" height="18" rx="6" {o("#5a4033", 5)}/></g>', (106, 288)),
    L("body", "\n".join([
        L("wool", wool),
        L("ear-left", f'<ellipse cx="116" cy="200" rx="38" ry="17" transform="rotate(-28 116 200)" {o("#c79a74")}/>', (140, 192)),
        L("ear-right", f'<ellipse cx="284" cy="200" rx="38" ry="17" transform="rotate(28 284 200)" {o("#c79a74")}/>', (260, 192)),
        L("face-base", f'<ellipse cx="200" cy="208" rx="80" ry="64" {o("#f1d9bf")}/>'),
        L("tuft", "".join(f'<circle cx="{x}" cy="{y}" r="20" {o(WOOL)}/>' for x, y in [(170, 148), (200, 138), (230, 148)])
                  + "".join(f'<circle cx="{x}" cy="{y}" r="16.5" fill="{WOOL}"/>' for x, y in [(170, 148), (200, 138), (230, 148)]), (200, 150)),
        eyes(212, dx=36, rx=9, ry=13),
        blush(236, dx=58),
        L("mouth", f'<path d="M188,238 q6,7 12,0 q6,7 12,0" {line(4)}/>', (200, 238)),
    ]), (200, 437)),
    L("arm-right", f'<g transform="rotate(-28 294 288)"><circle cx="294" cy="320" r="26" {o(WOOL)}/>'
                   f'<rect x="282" y="336" width="24" height="18" rx="6" {o("#5a4033", 5)}/></g>', (294, 288)),
])

# 5. BUBBLES - axolotl
AX = "#f7a8c4"
GILL = "#e2678f"


def gills(side):
    s = ""
    for (cx, cy, a) in [(74, 140, 28), (62, 188, 0), (74, 236, -28)]:
        if side == "right":
            cx, a = 400 - cx, -a
        s += f'<ellipse cx="{cx}" cy="{cy}" rx="36" ry="14" transform="rotate({a} {cx} {cy})" {o(GILL)}/>'
        s += f'<circle cx="{cx + (-12 if side == "left" else 12)}" cy="{cy}" r="3.5" fill="#fff" opacity=".7"/>'
    return L(f"gills-{side}", s, (104 if side == "left" else 296, 188))


chars["bubbles"] = ("Bubbles (axolotl)", [
    shadow(),
    L("tail", f'<path d="M290,400 C340,410 380,380 388,330 C360,350 330,355 296,350 Z" {o(AX)}/>'
              f'<path d="M300,380 C330,382 360,368 376,346" {line(4, GILL)}/>', (296, 380)),
    gills("left"), gills("right"),
    *blob_feet(AX),
    blob_arm("left", AX),
    L("body", "\n".join([
        L("body-base", f'<path d="{BLOB}" {o(AX)}/>'
                       f'<g clip-path="url(#bubbles-clip)"><ellipse cx="200" cy="390" rx="80" ry="66" fill="#fcd3e1" stroke="{INK}" stroke-width="5"/></g>'
                       f'<path d="{BLOB}" fill="none" stroke="{INK}" stroke-width="7"/>'),
        L("spots", "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GILL}" opacity=".55"/>'
                           for x, y, r in [(150, 128, 7), (170, 115, 4), (250, 125, 6), (268, 145, 4)])),
        eyes(200, dx=64, rx=10, ry=12),
        blush(232, dx=88),
        L("mouth", f'<path d="M160,228 Q200,262 240,228" {line(5)}/>', (200, 240)),
    ]), (200, 437)),
    blob_arm("right", AX),
], f'<clipPath id="bubbles-clip"><path d="{BLOB}"/></clipPath>')

# 6. GLOOP - slime monster, one big eye
SL = "#8bd86f"
SLIME = ("M95,250 C95,140 140,95 200,95 C260,95 305,140 305,250 L306,360 C306,385 318,400 334,414 "
         "C350,430 338,446 312,446 L88,446 C62,446 50,430 66,414 C82,400 94,385 94,360 Z")
chars["gloop"] = ("Gloop (slime monster)", [
    shadow(rx=135, cy=460),
    L("puddle", f'<ellipse cx="200" cy="446" rx="150" ry="16" {o("#5fb44a")}/>', (200, 446)),
    blob_arm("left", SL, extra=f'<path d="M100,345 q6,18 0,24 q-6,-6 0,-24 Z" {o(SL, 4)}/>'),
    L("body", "\n".join([
        L("body-base", f'<path d="{SLIME}" {o(SL)}/>'
                       f'<ellipse cx="146" cy="150" rx="22" ry="12" transform="rotate(-35 146 150)" fill="#fff" opacity=".7"/>'
                       f'<circle cx="168" cy="132" r="5" fill="#fff" opacity=".7"/>'),
        L("bubbles", "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#4e9a3a" stroke-width="3" opacity=".6"/>'
                             for x, y, r in [(250, 360, 9), (140, 380, 6), (270, 300, 5), (130, 320, 4)])),
        L("drips", f'<path d="M300,250 q12,30 2,44 q-12,-8 -2,-44 Z" {o(SL, 5)}/>'
                   f'<path d="M110,220 q-10,26 -2,38 q10,-8 2,-38 Z" {o(SL, 5)}/>', (200, 250)),
        L("eye", f'<circle cx="200" cy="205" r="50" {o("#fff")}/>'
                 f'<circle cx="206" cy="212" r="22" fill="{INK}"/><circle cx="214" cy="202" r="7" fill="#fff"/>', (200, 205)),
        L("mouth", f'<path d="M148,292 Q200,338 252,292 Q200,306 148,292 Z" {o("#3a1f2a", 5)}/>'
                   f'<path d="M210,312 q14,-8 22,-4 q-2,14 -16,14 Z" fill="#f2789a"/>', (200, 305)),
    ]), (200, 446)),
    blob_arm("right", SL, extra=f'<path d="M300,345 q6,18 0,24 q-6,-6 0,-24 Z" {o(SL, 4)}/>'),
])

# 7. GRUMBLE - horned monster with tiny bat wings and fangs
GR = "#8c6ad6"
DK = "#5d4396"
chars["grumble"] = ("Grumble (horned monster)", [
    shadow(),
    L("wing-left", f'<path d="M112,250 C62,205 26,226 20,270 C42,264 48,292 70,288 C74,310 96,312 108,300 Z" {o(DK)}/>'
                   f'<path d="M108,262 L48,262 M108,280 L74,292" {line(4, "#3c2b66")}/>', (108, 270)),
    L("wing-right", f'<path d="M288,250 C338,205 374,226 380,270 C358,264 352,292 330,288 C326,310 304,312 292,300 Z" {o(DK)}/>'
                    f'<path d="M292,262 L352,262 M292,280 L326,292" {line(4, "#3c2b66")}/>', (292, 270)),
    L("horn-left", f'<path d="M128,118 C98,96 88,56 108,26 C120,64 146,90 166,96 Z" {o("#f4e6c8")}/>'
                   f'<path d="M104,62 q14,4 22,-2 M112,88 q14,2 22,-6" {line(4, "#c9b48e")}/>', (140, 105)),
    L("horn-right", f'<path d="M272,118 C302,96 312,56 292,26 C280,64 254,90 234,96 Z" {o("#f4e6c8")}/>'
                    f'<path d="M296,62 q-14,4 -22,-2 M288,88 q-14,2 -22,-6" {line(4, "#c9b48e")}/>', (260, 105)),
    *blob_feet(DK),
    blob_arm("left", GR),
    L("body", "\n".join([
        L("body-base", f'<path d="{BLOB}" {o(GR)}/>'),
        L("spots", "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#a98ce6"/>'
                           for x, y, r in [(150, 340, 16), (240, 372, 22), (200, 318, 9), (262, 320, 8), (166, 392, 9)])),
        L("brows", f'<path d="M140,166 L178,180 M260,166 L222,180" {line(7)}/>', (200, 172)),
        eyes(200, dx=40, rx=12, ry=14),
        L("mouth", f'<path d="M140,250 Q200,286 260,250" {line(6)}/>'
                   f'<path d="M162,262 L170,236 L180,268 Z" {o("#fff", 5)}/>'
                   f'<path d="M220,268 L230,236 L238,262 Z" {o("#fff", 5)}/>', (200, 262)),
    ]), (200, 437)),
    blob_arm("right", GR),
])

# 8. WISP - little ghost carrying a lantern
GH = "#eef0ff"
GHOST = ("M100,170 C100,105 140,88 200,88 C260,88 300,105 300,170 L305,350 Q286,392 262,364 "
         "Q240,398 215,368 Q190,400 168,368 Q145,398 122,364 Q104,388 95,350 Z")
chars["wisp"] = ("Wisp (ghost)", [
    shadow(rx=70, cy=466),
    L("arm-left", f'<g transform="rotate(30 108 250)"><rect x="89" y="240" width="38" height="56" rx="19" {o(GH)}/></g>', (108, 250)),
    L("body", "\n".join([
        L("flame", f'<path d="M196,92 C182,66 214,54 206,30 C232,52 228,80 208,92 Z" {o("#c7cdfa")}/>', (202, 90)),
        L("body-base", f'<path d="{GHOST}" {o(GH)}/>'
                       f'<path d="M270,140 C282,180 284,260 280,320" {line(5, "#c7cdfa")}/>'),
        eyes(196, dx=40, rx=9, ry=13),
        blush(228, dx=66, color="#b6a3f5"),
        L("mouth", f'<ellipse cx="200" cy="232" rx="7" ry="8" {o("#4b3a6b", 4)}/>', (200, 232)),
    ]), (200, 380)),
    L("prop-lantern", f'<g transform="translate(-11,-14)"><path d="M318,322 q0,-26 22,-26 q22,0 22,26" {line(5)}/>'
                      f'<circle cx="340" cy="362" r="46" fill="#ffe9a0" opacity=".35"/>'
                      f'<rect x="316" y="322" width="48" height="66" rx="10" {o("#e9a23b")}/>'
                      f'<rect x="326" y="334" width="28" height="42" rx="6" {o("#fff3b8", 4)}/>'
                      f'<path d="M340,366 q-8,-10 0,-22 q8,12 0,22 Z" fill="#f08a3c"/></g>', (329, 282)),
    L("arm-right", f'<g transform="rotate(-50 292 250)"><rect x="273" y="240" width="38" height="58" rx="19" {o(GH)}/></g>', (292, 250)),
])


# ---------- write files ---------------------------------------------------------
os.makedirs(OUT, exist_ok=True)
order = list(chars)
inline = []
for key in order:
    title, layers, *rest = chars[key]
    s = svg(key, title, layers, rest[0] if rest else "")
    with open(os.path.join(OUT, f"{key}.svg"), "w") as f:
        f.write(s)
    inline.append((key, title, s.split("\n", 0)[0]))

cards = "\n".join(
    f'<figure class="card"><div class="stage">{s}</div><figcaption>{t}</figcaption></figure>'
    for k, t, s in inline)

PREVIEW = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chibi Character Lineup</title>
<style>
  :root { --bg:#f6f1e7; --card:#fffdf8; --ink:#1d1a1a; --muted:#6c645a; }
  @media (prefers-color-scheme: dark) { :root { --bg:#1e1c22; --card:#2a2730; --ink:#f3efe7; --muted:#a59fb0; } }
  * { box-sizing:border-box; }
  body { margin:0; padding:24px 16px; background:var(--bg); color:var(--ink);
         font:16px/1.4 system-ui, sans-serif; }
  h1 { margin:0 0 4px; font-size:22px; }
  p { margin:0 0 20px; color:var(--muted); }
  .grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:16px; }
  .card { margin:0; background:var(--card); border-radius:16px; padding:12px; }
  .stage svg { width:100%; height:auto; display:block; overflow:visible; }
  figcaption { text-align:center; font-weight:600; margin-top:4px; }
  label { display:inline-flex; gap:6px; align-items:center; margin-bottom:16px; color:var(--muted); }

  .anim svg { animation: bob 1.6s ease-in-out infinite; }
  .anim .L-eyes, .anim .L-eye { animation: blink 4s infinite; }
  .anim .L-arm-right { animation: wave 1.2s ease-in-out infinite; }
  .anim .L-arm-left { animation: sway 1.6s ease-in-out infinite; }
  .anim .L-tail { animation: wag .9s ease-in-out infinite alternate; }
  .anim .L-gills-left { animation: wag .7s ease-in-out infinite alternate; }
  .anim .L-gills-right { animation: wag .7s ease-in-out infinite alternate-reverse; }
  .anim .L-wing-left { animation: flapL .35s ease-in-out infinite alternate; }
  .anim .L-wing-right { animation: flapR .35s ease-in-out infinite alternate; }
  .anim .L-ear-left, .anim .L-ear-right { animation: wag 1.8s ease-in-out infinite alternate; }
  .anim .L-head { animation: tilt 3s ease-in-out infinite; }
  .anim .L-body { animation: squash 1.6s ease-in-out infinite; }
  .anim .L-prop-lantern { animation: swing 1.4s ease-in-out infinite alternate; }
  .anim .L-flame { animation: wag .5s ease-in-out infinite alternate; }
  @keyframes bob { 50% { transform: translateY(-6px); } }
  @keyframes blink { 0%, 92%, 100% { transform: scaleY(1); } 95% { transform: scaleY(.1); } }
  @keyframes wave { 50% { transform: rotate(-35deg); } }
  @keyframes sway { 50% { transform: rotate(8deg); } }
  @keyframes wag { from { transform: rotate(-6deg); } to { transform: rotate(6deg); } }
  @keyframes flapL { to { transform: rotate(-18deg); } }
  @keyframes flapR { to { transform: rotate(18deg); } }
  @keyframes tilt { 25% { transform: rotate(-3deg); } 75% { transform: rotate(3deg); } }
  @keyframes squash { 50% { transform: scale(1.03, .97); } }
  @keyframes swing { from { transform: rotate(-8deg); } to { transform: rotate(8deg); } }
  @media (prefers-reduced-motion: reduce) { .anim * { animation: none !important; } }
</style></head>
<body class="anim">
<h1>Chibi character lineup</h1>
<p>Eight original characters. Each part is its own layer with a pivot point; the motion here is plain CSS driving those layers.</p>
<label><input type="checkbox" id="toggle" checked> Animate</label>
<div class="grid">
__CARDS__
</div>
<script>
  // Set each layer's transform origin from its data-pivot (in SVG user units).
  document.querySelectorAll('[data-pivot]').forEach(function (g) {
    var p = g.getAttribute('data-pivot').split(' ');
    g.style.transformBox = 'view-box';
    g.style.transformOrigin = p[0] + 'px ' + p[1] + 'px';
  });
  document.getElementById('toggle').addEventListener('change', function (e) {
    document.body.classList.toggle('anim', e.target.checked);
  });
</script>
</body></html>
"""
with open(os.path.join(HERE, "preview.html"), "w") as f:
    f.write(PREVIEW.replace("__CARDS__", cards))
print("wrote", len(order), "characters")
