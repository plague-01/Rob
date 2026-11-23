#!/usr/bin/env python3
"""Four soft chibi kittens in a pencil-and-watercolour feel: round mochi heads,
tiny bodies, toe-bean paws, wobbly thin outlines (SVG displacement filter),
blurred colour patches and paper grain.

Writes svg/mochi-<name>.svg (layered, 400x400) and mochi-kittens.svg (2x2 sheet).
Run: python3 mochi_kittens.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#4a3a35"
BEAN = "#eea6a6"
HEAD_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"')


def filters(p):
    """Hand-drawn wobble for lines, soft edges for paint, blur for colour patches."""
    return (f'<filter id="{p}wobble" x="-5%" y="-5%" width="110%" height="110%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4"/>'
            f'<feDisplacementMap in="SourceGraphic" scale="3.2"/></filter>'
            f'<filter id="{p}paint" x="-5%" y="-5%" width="110%" height="110%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="9"/>'
            f'<feDisplacementMap in="SourceGraphic" scale="2.5"/></filter>'
            f'<filter id="{p}soft" x="-30%" y="-30%" width="160%" height="160%">'
            f'<feGaussianBlur stdDeviation="7"/></filter>')


def L(name, content, pivot=None):
    piv = f' data-pivot="{pivot[0]:.0f} {pivot[1]:.0f}"' if pivot else ""
    return (f'<g id="{name}" class="L-{name}" inkscape:groupmode="layer" '
            f'inkscape:label="{name}"{piv}>\n{content}\n</g>')


class K:
    """Drawing helpers bound to one kitten's id prefix."""

    def __init__(self, p, ink=INK):
        self.p, self.ink = p, ink

    def ln(self, w=3.2, color=None):
        return (f'fill="none" stroke="{color or self.ink}" stroke-width="{w}" '
                f'stroke-linecap="round" stroke-linejoin="round" filter="url(#{self.p}wobble)"')

    def part(self, name, d, fill, patches=""):
        cid = f"{self.p}{name}-clip"
        return (f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
                f'<path d="{d}" fill="{fill}" filter="url(#{self.p}paint)"/>'
                f'<g clip-path="url(#{cid})"><g filter="url(#{self.p}soft)">{patches}</g></g>'
                f'<path d="{d}" {self.ln()}/>')

    def oval(self, name, cx, cy, rx, ry, fill, patches="", rot=0):
        # an ellipse as a path so it can share part()
        d = (f"M{cx - rx},{cy} A{rx},{ry} 0 1 0 {cx + rx},{cy} A{rx},{ry} 0 1 0 {cx - rx},{cy} Z")
        body = self.part(name, d, fill, patches)
        return f'<g transform="rotate({rot} {cx} {cy})">{body}</g>' if rot else body

    def tail(self, d, fill, w=13):
        return (f'<path d="{d}" fill="none" stroke="{self.ink}" stroke-width="{w + 6.4}" '
                f'stroke-linecap="round" filter="url(#{self.p}wobble)"/>'
                f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{w}" stroke-linecap="round"/>')

    def foot(self, name, cx, cy, fill, tip=None):
        beans = (f'<ellipse cx="{cx}" cy="{cy + 3}" rx="7.5" ry="5.5" fill="{BEAN}"/>'
                 + "".join(f'<circle cx="{cx + dx}" cy="{cy - 7 + abs(dx) * .25}" r="2.8" fill="{BEAN}"/>'
                           for dx in (-8, 0, 8)))
        patch = f'<ellipse cx="{cx}" cy="{cy + 14}" rx="26" ry="12" fill="{tip}"/>' if tip else ""
        return self.oval(name, cx, cy, 22, 17, fill, patch) + beans


# ---- shared head ------------------------------------------------------------------
HEAD = ("M110,190 C106,130 150,98 200,98 C250,98 294,130 290,190 "
        "C288,240 250,262 200,262 C150,262 112,240 110,190 Z")
EAR_L = "M128,148 C120,118 124,92 134,78 C152,88 170,102 182,118 Z"
EAR_R = "M272,148 C280,118 276,92 266,78 C248,88 230,102 218,118 Z"
EAR_IN_L = "M138,130 C135,113 137,101 141,93 C151,100 159,108 165,116 Z"
EAR_IN_R = "M262,130 C265,113 263,101 259,93 C249,100 241,108 235,116 Z"


def head(k, c, eyes="open", mouth="w", tilt=0, at=(0, 0), scale=1.0):
    ear_fill = c.get("ear", c["base"])
    ear_in = c.get("ear_in", "#f2b8b8")
    ear_p = c.get("ear_p", "")
    ears = (k.part("earl", EAR_L, ear_fill, ear_p) + f'<path d="{EAR_IN_L}" fill="{ear_in}" opacity=".85"/>'
            + k.part("earr", EAR_R, ear_fill, ear_p) + f'<path d="{EAR_IN_R}" fill="{ear_in}" opacity=".85"/>')
    eye_col = c.get("eye", "#3a2c28")
    if eyes == "open":
        e = "".join(f'<circle cx="{x}" cy="190" r="7.5" fill="{eye_col}"/>'
                    f'<circle cx="{x + 2.5}" cy="187" r="2.4" fill="#fff"/>' for x in (164, 236))
    elif eyes == "happy":
        e = "".join(f'<path d="M{x - 9},194 q9,-10 18,0" {k.ln(3.4, c.get("lid"))}/>' for x in (164, 236))
    else:  # sleepy
        e = "".join(f'<path d="M{x - 9},190 q9,8 18,0" {k.ln(3.4, c.get("lid"))}/>' for x in (164, 236))
    m = {
        "w": f'<path d="M189,210 q5.5,6 11,0 q5.5,6 11,0" {k.ln(2.6, c.get("lid"))}/>',
        "open": (f'<path d="M190,208 q10,3 20,0 q-2,16 -10,16 q-8,0 -10,-16 Z" fill="#e98a8f" '
                 f'stroke="{c.get("lid", INK)}" stroke-width="2.4" stroke-linejoin="round"/>'),
    }[mouth]
    face = (L("eyes", e, (200, 190))
            + L("mouth", f'<path d="M196,203 h8 l-4,3.5 Z" fill="#d98c8c"/>' + m, (200, 210))
            + L("blush", f'<g filter="url(#{k.p}soft)"><ellipse cx="146" cy="214" rx="16" ry="8" fill="#f4a3a3" opacity=".6"/>'
                         f'<ellipse cx="254" cy="214" rx="16" ry="8" fill="#f4a3a3" opacity=".6"/></g>')
            + L("whiskers", f'<path d="M110,200 l-16,-3 M111,210 l-16,3 M290,200 l16,-3 M289,210 l16,3" {k.ln(2)}/>'))
    inner = ears + k.part("head", HEAD, c["base"], c.get("head_p", "")) + face
    tx = (f'translate({at[0]},{at[1]}) rotate({tilt} 200 230) '
          f'translate(200,230) scale({scale}) translate(-200,-230)')
    return L("head", f'<g transform="{tx}">{inner}</g>', (200 + at[0], 250 + at[1]))


def sitting_body(k, c):
    d = ("M150,246 C136,276 134,318 144,338 C150,350 170,353 200,353 "
         "C230,353 250,350 256,338 C266,318 264,276 250,246 Z")
    return L("body", k.part("body", d, c["base"], c.get("body_p", "")), (200, 352))


def ground(cx=200, rx=95, cy=362):
    return L("shadow", f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="9" fill="#9aa8c0" opacity=".22"/>')


# ---- the four kittens -------------------------------------------------------------
def mochi():
    """White kitten with peach ear tips, holding a strawberry."""
    k = K("mochi-")
    c = dict(base="#fdf6ee", ear="#fdf6ee",
             ear_p='<ellipse cx="134" cy="80" rx="30" ry="30" fill="#efbf9c"/>'
                   '<ellipse cx="266" cy="80" rx="30" ry="30" fill="#efbf9c"/>',
             head_p='<ellipse cx="200" cy="100" rx="40" ry="14" fill="#f3d2ba"/>')
    berry = (f'<path d="M184,286 C176,300 184,326 200,334 C216,326 224,300 216,286 C206,280 194,280 184,286 Z" '
             f'fill="#ef6b6b" filter="url(#{k.p}paint)"/>'
             f'<path d="M184,286 C176,300 184,326 200,334 C216,326 224,300 216,286 C206,280 194,280 184,286 Z" {k.ln(2.8)}/>'
             + "".join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#ffe08a"/>'
                       for x, y in [(192, 298), (205, 296), (198, 310), (210, 312), (194, 320), (204, 324)])
             + f'<path d="M188,286 l6,-10 l6,8 l6,-8 l6,10 Z" fill="#7cbf7a"/><path d="M188,286 l6,-10 l6,8 l6,-8 l6,10" {k.ln(2.4)}/>')
    return [
        ground(),
        L("tail", k.tail("M250,336 C290,340 304,314 294,290", "#efbf9c"), (250, 336)),
        sitting_body(k, c),
        L("foot-left", k.foot("footl", 170, 346, c["base"]), (170, 340)),
        L("foot-right", k.foot("footr", 230, 346, c["base"]), (230, 340)),
        L("prop-strawberry", berry, (200, 306)),
        L("arm-left", k.oval("arml", 182, 300, 13, 16, c["base"], rot=-20), (176, 286)),
        L("arm-right", k.oval("armr", 218, 300, 13, 16, c["base"], rot=20), (224, 286)),
        head(k, c, eyes="open", mouth="open"),
    ]


def kuro():
    """Black kitten with amber eyes and a little bell collar."""
    k = K("kuro-", ink="#231c1d")
    c = dict(base="#3a3236", ear_in="#8a6f75", eye="#e9b949", lid="#f1e4d8",
             head_p='<ellipse cx="170" cy="130" rx="40" ry="20" fill="#5c5258"/>')
    collar = (f'<path d="M150,252 C175,266 225,266 250,252" fill="none" stroke="#d9636a" stroke-width="10" stroke-linecap="round"/>'
              f'<circle cx="200" cy="268" r="10" fill="#f2c94c"/><circle cx="200" cy="268" r="10" {k.ln(2.6)}/>'
              f'<path d="M193,268 h14 M200,270 v6" {k.ln(2.2)}/>')
    return [
        ground(),
        L("tail", k.tail("M252,336 C296,336 312,300 300,270 C296,260 304,252 312,256", c["base"]), (252, 336)),
        sitting_body(k, c),
        L("foot-left", k.foot("footl", 170, 346, c["base"]), (170, 340)),
        L("foot-right", k.foot("footr", 230, 346, c["base"]), (230, 340)),
        head(k, c, eyes="open", mouth="w", tilt=-5),
        L("collar", collar, (200, 262)),
    ]


def sumi():
    """Soft gray tabby, napping in a loaf."""
    k = K("sumi-")
    G, GD = "#c9c4c0", "#9a938e"
    c = dict(base=G,
             head_p=(f'<path d="M184,104 l4,22 M200,100 v26 M216,104 l-4,22" stroke="{GD}" stroke-width="9" stroke-linecap="round"/>'
                     f'<ellipse cx="200" cy="232" rx="56" ry="30" fill="#f1eeeb"/>'))
    body_d = ("M120,318 C108,268 156,242 226,244 C302,246 334,276 328,322 "
              "C324,346 296,354 258,354 L150,354 C128,354 122,340 120,318 Z")
    body_p = "".join(f'<path d="M{x},248 l-8,30" stroke="{GD}" stroke-width="12" stroke-linecap="round"/>'
                     for x in (250, 280, 306))
    zz = (f'<text x="292" y="150" font-family="Georgia, serif" font-style="italic" font-size="26" fill="#8fa3c7">z</text>'
          f'<text x="314" y="124" font-family="Georgia, serif" font-style="italic" font-size="18" fill="#8fa3c7">z</text>')
    return [
        ground(220, 120),
        L("body", k.part("body", body_d, G, body_p), (226, 354)),
        L("tail", k.tail("M322,336 C312,360 262,362 238,356", G), (322, 336)),
        L("paws", k.oval("pawl", 158, 350, 20, 11, "#f1eeeb") + k.oval("pawr", 196, 352, 20, 11, "#f1eeeb"), (176, 350)),
        head(k, c, eyes="sleepy", mouth="w", tilt=-8, at=(-20, 70), scale=.86),
        L("zzz", zz),
    ]


def kinako():
    """Ginger kitten waving hello."""
    k = K("kinako-")
    O, OL = "#f0c08b", "#fbeedd"
    c = dict(base=O,
             head_p=(f'<ellipse cx="200" cy="236" rx="62" ry="34" fill="{OL}"/>'
                     f'<path d="M186,104 l3,20 M200,101 v24 M214,104 l-3,20" stroke="#d99358" stroke-width="8" stroke-linecap="round"/>'),
             body_p=f'<ellipse cx="200" cy="300" rx="36" ry="50" fill="{OL}"/>')
    return [
        ground(),
        L("tail", k.tail("M252,336 C292,340 310,316 300,292", O)
                  + f'<path d="M280,340 l4,-12 M298,322 l-10,-6" stroke="#d99358" stroke-width="5" stroke-linecap="round"/>', (252, 336)),
        sitting_body(k, c),
        L("foot-left", k.foot("footl", 170, 346, OL), (170, 340)),
        L("foot-right", k.foot("footr", 230, 346, OL), (230, 340)),
        head(k, c, eyes="happy", mouth="open", tilt=6),
        # waving paw, palm forward with beans
        L("arm-right", k.oval("armr", 304, 214, 15, 21, O, rot=-18)
                       + f'<ellipse cx="306" cy="209" rx="6.5" ry="5.5" fill="{BEAN}"/>'
                       + "".join(f'<circle cx="{x}" cy="{y}" r="2.4" fill="{BEAN}"/>' for x, y in [(298, 199), (306, 196), (314, 200)]),
          (284, 240)),
    ]


KITTENS = {
    "mochi": ("Mochi (with a strawberry)", mochi),
    "kuro": ("Kuro (black, bell collar)", kuro),
    "sumi": ("Sumi (napping tabby)", sumi),
    "kinako": ("Kinako (waving ginger)", kinako),
}

os.makedirs(os.path.join(HERE, "svg"), exist_ok=True)
built = {}
for key, (title, fn) in KITTENS.items():
    content = "\n".join(fn())
    built[key] = content
    with open(os.path.join(HERE, "svg", f"mochi-{key}.svg"), "w") as f:
        f.write(f'{HEAD_SVG} viewBox="0 0 400 400" width="400" height="400" data-character="{key}">\n'
                f'<title>{title}</title>\n<defs>{filters(key + "-")}</defs>\n{content}\n</svg>\n')

paper = ('<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="2"/>'
         '<feColorMatrix values="0 0 0 0 0.35  0 0 0 0 0.4  0 0 0 0 0.5  0 0 0 0.09 0"/></filter>')
defs = paper + "".join(filters(k + "-") for k in KITTENS)
cells = ""
for i, key in enumerate(KITTENS):
    x, y = (i % 2) * 400, (i // 2) * 420
    cells += (f'<g transform="translate({x},{y})">{built[key]}'
              f'<text x="200" y="396" text-anchor="middle" font-family="Georgia, serif" '
              f'font-size="19" fill="#5d4c47">{KITTENS[key][0]}</text></g>')
with open(os.path.join(HERE, "mochi-kittens.svg"), "w") as f:
    f.write(f'{HEAD_SVG} viewBox="0 0 800 840" width="800" height="840">\n<title>Mochi kittens</title>\n'
            f'<defs>{defs}</defs>\n<rect width="800" height="840" fill="#f4f7f9"/>\n'
            f'<rect width="800" height="840" filter="url(#grain)"/>\n{cells}\n</svg>\n')
print("wrote", ", ".join(f"svg/mochi-{k}.svg" for k in KITTENS), "and mochi-kittens.svg")
