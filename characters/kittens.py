#!/usr/bin/env python3
"""Four illustrated kittens: slim bodies, tall ears, big colored eyes, cheek tufts,
thin brown outlines and soft lavender shading. Each in a different pose.

Writes svg/kitten-<name>.svg (layered, 400x400) and kittens.svg (2x2 sheet).
Run: python3 kittens.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#3b2a26"
SHADE = "#5b4a86"
GROUND = "#d9d2ea"
OW = 4.5  # outline width
HEAD_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"')


def line(w=OW, color=INK):
    return f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'


def L(name, content, pivot=None):
    piv = f' data-pivot="{pivot[0]:.0f} {pivot[1]:.0f}"' if pivot else ""
    return (f'<g id="{name}" class="L-{name}" inkscape:groupmode="layer" '
            f'inkscape:label="{name}"{piv}>\n{content}\n</g>')


def part(cid, d, fill, patches="", outline=None, w=OW):
    """Filled shape + patches clipped inside it + outline on top."""
    return (f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
            f'<path d="{d}" fill="{fill}"/>'
            f'<g clip-path="url(#{cid})">{patches}</g>'
            f'<path d="{outline or d}" {line(w)}/>')


def shade(d_or_shape):
    return f'<g fill="{SHADE}" opacity=".16">{d_or_shape}</g>'


def noodle(cid, d, fill, w=22, patches=""):
    """Thick outlined stroke (tail), with optional patches masked to the stroke."""
    return (f'<mask id="{cid}" maskUnits="userSpaceOnUse" x="0" y="0" width="400" height="400">'
            f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{w}" stroke-linecap="round"/></mask>'
            f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 2 * OW}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<g mask="url(#{cid})">{patches}</g>')


def leg(x, top, bottom, w=22):
    """Slim leg with a rounded paw. Returns (closed fill path, open outline path)."""
    r = w / 2
    o = (f"M{x},{top} V{bottom - r} C{x},{bottom - 2} {x + 3},{bottom} {x + r},{bottom} "
         f"C{x + w - 3},{bottom} {x + w},{bottom - 2} {x + w},{bottom - r} V{top}")
    return o + " Z", o


def leg_part(cid, x, top, bottom, fill, patches="", w=22):
    closed, open_d = leg(x, top, bottom, w)
    toes = f'<path d="M{x + w * .36:.1f},{bottom} v-7 M{x + w * .64:.1f},{bottom} v-7" {line(3)}/>'
    return part(cid, closed, fill, patches, outline=open_d) + toes


# ---- head (local coords, centre 0,0) ------------------------------------------
HEAD = ("M-58,0 C-60,-38 -34,-52 0,-52 C34,-52 60,-38 58,0 L68,8 L57,15 L64,26 L46,29 "
        "C30,44 -30,44 -46,29 L-64,26 L-57,15 L-68,8 Z")
EAR_L = "M-50,-24 L-60,-96 C-40,-84 -22,-64 -12,-48 Z"
EAR_R = "M50,-24 L60,-96 C40,-84 22,-64 12,-48 Z"
EAR_IN_L = "M-45,-34 L-53,-82 C-41,-72 -30,-60 -22,-48 Z"
EAR_IN_R = "M45,-34 L53,-82 C41,-72 30,-60 22,-48 Z"


def head(key, cx, cy, rot, c, eyes="open", mouth="smile"):
    base, ear_in = c["base"], c.get("ear_in", "#f2c2c4")
    ear = lambda d, di: (f'<path d="{d}" fill="{c.get("ear", base)}"/>'
                         f'<path d="{di}" fill="{ear_in}"/>'
                         f'<path d="{d}" {line()}/>')
    tufts = (f'<path d="M-44,-46 l4,10 M-38,-52 l2,12" {line(2.5)}/>'
             f'<path d="M44,-46 l-4,10 M38,-52 l-2,12" {line(2.5)}/>')
    if eyes == "open":
        iris = c["eye"]
        e = ""
        for x in (-24, 24):
            e += (f'<ellipse cx="{x}" cy="4" rx="13" ry="15" fill="{iris}" stroke="{INK}" stroke-width="3.5"/>'
                  f'<ellipse cx="{x + 1}" cy="6" rx="5.5" ry="10" fill="#1d1715"/>'
                  f'<circle cx="{x + 5}" cy="-3" r="4" fill="#fff"/><circle cx="{x - 4}" cy="11" r="1.8" fill="#fff"/>'
                  f'<path d="M{x - 13},4 A13,15 0 0 1 {x + 13},4" {line(5.5)}/>')
    else:
        e = "".join(f'<path d="M{x - 12},6 Q{x},14 {x + 12},6" {line(4.5)}/>' for x in (-24, 24))
    m = {
        "smile": f'<path d="M-7,25 q3.5,5 7,0 q3.5,5 7,0" {line(3.5)}/>',
        "o": f'<ellipse cx="0" cy="28" rx="5" ry="6.5" fill="#8a3f44" stroke="{INK}" stroke-width="3"/>',
        "flat": f'<path d="M-6,26 q6,4 12,0" {line(3.5)}/>',
    }[mouth]
    face = (L("eyes", e, (0, 4)) +  # pivot in head-local coords
            L("nose", f'<path d="M-4.5,16 h9 l-4.5,5 Z" fill="#e19a9c" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>') +
            L("mouth", m) +
            L("blush", '<ellipse cx="-38" cy="20" rx="9" ry="5" fill="#f2a0a8" opacity=".45"/>'
                       '<ellipse cx="38" cy="20" rx="9" ry="5" fill="#f2a0a8" opacity=".45"/>'))
    body = (ear(EAR_L, EAR_IN_L) + ear(EAR_R, EAR_IN_R)
            + part(f"{key}-head-clip", HEAD, base,
                   c.get("head_p", "") + shade('<ellipse cx="0" cy="40" rx="62" ry="14"/>'))
            + tufts + face)
    return L("head", f'<g transform="translate({cx},{cy}) rotate({rot}) scale(1.2)">{body}</g>', (cx, cy + 48))


def ground(cx, cy, rx):
    return L("shadow", f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="11" fill="{GROUND}"/>')


# ---- the four kittens ----------------------------------------------------------
def biscuit():
    """Cream-orange tabby, sitting, blue eyes."""
    k = "biscuit"
    c = dict(base="#f4c48c", eye="#62a9dc",
             head_p=('<path d="M-30,44 C-34,20 -16,8 0,12 C16,8 34,20 30,44 Z" fill="#fff4e6"/>'
                     f'<path d="M-10,-48 l2,14 M0,-51 v16 M10,-48 l-2,14 M-60,-6 l14,2 M60,-6 l-14,2" {line(5, "#d68a46")}/>'))
    body_d = ("M170,175 C150,225 140,290 146,330 C148,346 160,352 176,352 L244,352 "
              "C266,352 276,340 272,318 C266,276 250,214 232,175 Z")
    body_p = ('<ellipse cx="203" cy="236" rx="26" ry="46" fill="#fff4e6"/>'
              f'<path d="M262,246 l-14,6 M268,276 l-16,5 M272,306 l-16,4" {line(6, "#d68a46")}/>'
              + shade('<ellipse cx="262" cy="330" rx="40" ry="44"/>'))
    tail_d = "M250,346 C292,352 326,352 337,334 C345,320 335,306 323,314"
    return [
        ground(220, 354, 110),
        L("tail", noodle(f"{k}-tail-m", tail_d, "#f4c48c",
                         patches=f'<path d="M288,340 v18 M312,336 v18 M332,326 l-14,8" {line(7, "#d68a46")}/>'), (250, 346)),
        L("body", part(f"{k}-body-clip", body_d, "#f4c48c", body_p)
                  + f'<path d="M244,352 C240,318 256,296 276,306" {line()}/>', (210, 352)),
        L("leg-left", leg_part(f"{k}-legl", 176, 250, 355, "#fff4e6"), (187, 250)),
        L("leg-right", leg_part(f"{k}-legr", 206, 250, 355, "#fff4e6"), (217, 250)),
        head(k, 202, 132, -4, c, mouth="smile"),
    ]


def juniper():
    """Tuxedo, standing side-on mid-step, green eyes."""
    k = "juniper"
    BLK, DK, WH = "#3b3638", "#2a2628", "#fbf7f2"
    c = dict(base=BLK, eye="#a8d25a", ear_in="#8d7a80",
             head_p=f'<path d="M-6,-34 L6,-34 L14,2 C34,10 42,30 32,46 L-32,46 C-42,30 -34,10 -14,2 Z" fill="{WH}"/>'
                    '<path d="M-40,-30 C-30,-40 -10,-44 4,-42" fill="none" stroke="#6a6266" stroke-width="5" stroke-linecap="round"/>')
    body_d = ("M118,205 C116,180 140,168 175,170 L250,168 C285,166 300,185 298,212 "
              "C296,240 276,254 250,254 L160,254 C132,254 120,234 118,205 Z")
    body_p = (f'<ellipse cx="200" cy="262" rx="78" ry="24" fill="{WH}"/>'
              f'<ellipse cx="136" cy="222" rx="22" ry="38" fill="{WH}"/>'
              '<path d="M170,184 C200,176 240,176 266,182" fill="none" stroke="#6a6266" stroke-width="6" stroke-linecap="round"/>')
    sock = lambda y: f'<rect x="0" y="{y}" width="400" height="80" fill="{WH}"/>'
    return [
        ground(205, 338, 120),
        L("leg-back-far", leg_part(f"{k}-lbf", 254, 220, 330, DK, sock(306), w=20), (264, 220)),
        L("leg-front-far", leg_part(f"{k}-lff", 156, 220, 330, DK, sock(306), w=20), (166, 220)),
        L("tail", noodle(f"{k}-tail-m", "M290,196 C330,182 338,130 318,104 C310,94 318,82 330,88", BLK, w=20), (290, 196)),
        L("body", part(f"{k}-body-clip", body_d, BLK, body_p), (210, 254)),
        L("leg-front-near", leg_part(f"{k}-lfn", 130, 222, 336, BLK, sock(300)), (141, 222)),
        L("leg-back-near", leg_part(f"{k}-lbn", 268, 222, 336, BLK, sock(304)), (279, 222)),
        head(k, 128, 140, -6, c, mouth="o"),
    ]


def smoke():
    """Blue-gray loaf with paws tucked, gold eyes."""
    k = "smoke"
    G, GD, GL = "#a3b0c2", "#7d8aa0", "#e6ebf2"
    c = dict(base=G, eye="#e8c547", ear_in="#dcc8d4",
             head_p=(f'<path d="M-30,44 C-34,22 -16,10 0,14 C16,10 34,22 30,44 Z" fill="{GL}"/>'
                     f'<path d="M-8,-48 l2,12 M8,-48 l-2,12 M-58,-4 l12,2 M58,-4 l-12,2" {line(5, GD)}/>'))
    body_d = ("M110,330 C100,262 150,228 222,226 C292,224 330,262 326,318 "
              "C324,334 310,340 290,340 L130,340 C116,340 111,336 110,330 Z")
    body_p = (f'<path d="M232,232 l-6,22 M262,236 l-8,22 M290,248 l-10,20" {line(7, GD)}/>'
              f'<ellipse cx="170" cy="300" rx="44" ry="40" fill="{GL}"/>'
              + shade('<ellipse cx="290" cy="320" rx="60" ry="30"/>'))
    paw = lambda cx: (f'<ellipse cx="{cx}" cy="340" rx="17" ry="10" fill="{GL}" stroke="{INK}" stroke-width="{OW}"/>'
                      f'<path d="M{cx - 4},346 v-6 M{cx + 4},346 v-6" {line(2.5)}/>')
    return [
        ground(218, 346, 130),
        L("body", part(f"{k}-body-clip", body_d, G, body_p), (218, 340)),
        L("tail", noodle(f"{k}-tail-m", "M318,334 C300,352 248,354 214,348", G, w=20,
                         patches=f'<path d="M290,350 v-16 M262,354 v-16" {line(6, GD)}/>'), (318, 334)),
        L("paws", paw(150) + paw(186), (168, 340)),
        head(k, 166, 224, 8, c, mouth="smile"),
    ]


def ember():
    """Tortoiseshell, curled up asleep."""
    k = "ember"
    D, O, OL = "#3f302c", "#e3893d", "#f2b46a"
    c = dict(base=D, ear_in="#a07870",
             head_p=(f'<ellipse cx="-38" cy="-30" rx="28" ry="22" fill="{O}"/>'
                     f'<path d="M-2,-60 C30,-50 70,-20 70,50 L-50,50 C-50,20 -30,4 -4,2 Z" fill="{OL}"/>'
                     f'<ellipse cx="-30" cy="18" rx="22" ry="14" fill="{O}"/>'))
    body_d = ("M90,290 C86,230 150,200 220,202 C292,204 330,240 326,292 "
              "C322,336 270,352 210,352 C140,352 94,336 90,290 Z")
    body_p = (f'<ellipse cx="240" cy="230" rx="50" ry="30" fill="{O}"/>'
              f'<ellipse cx="300" cy="290" rx="30" ry="40" fill="{OL}"/>'
              f'<ellipse cx="160" cy="330" rx="40" ry="20" fill="{O}"/>'
              + shade('<ellipse cx="220" cy="350" rx="130" ry="30"/>'))
    return [
        ground(210, 354, 130),
        L("body", part(f"{k}-body-clip", body_d, D, body_p), (210, 352)),
        L("tail", noodle(f"{k}-tail-m", "M318,300 C320,342 252,360 182,352 C150,348 130,342 120,332", D, w=24,
                         patches=f'<path d="M260,350 l6,-22 M220,358 l4,-22" stroke="{O}" stroke-width="14" stroke-linecap="round"/>'),
          (318, 300)),
        L("paw", f'<ellipse cx="196" cy="300" rx="20" ry="12" fill="{OL}" stroke="{INK}" stroke-width="{OW}"/>', (196, 300)),
        head(k, 148, 262, -18, c, eyes="closed", mouth="flat"),
        L("zzz", f'<text x="92" y="176" font-family="system-ui, sans-serif" font-size="26" font-weight="700" fill="{SHADE}" opacity=".55">z</text>'
                 f'<text x="70" y="150" font-family="system-ui, sans-serif" font-size="18" font-weight="700" fill="{SHADE}" opacity=".45">z</text>'),
    ]


KITTENS = {
    "biscuit": ("Biscuit (cream tabby)", biscuit),
    "juniper": ("Juniper (tuxedo)", juniper),
    "smoke": ("Smoke (blue-gray)", smoke),
    "ember": ("Ember (tortoiseshell)", ember),
}

os.makedirs(os.path.join(HERE, "svg"), exist_ok=True)
built = {}
for key, (title, fn) in KITTENS.items():
    content = "\n".join(fn())
    built[key] = content
    with open(os.path.join(HERE, "svg", f"kitten-{key}.svg"), "w") as f:
        f.write(f'{HEAD_SVG} viewBox="0 0 400 400" width="400" height="400" data-character="{key}">\n'
                f'<title>{title}</title>\n{content}\n</svg>\n')

cells = ""
for i, key in enumerate(KITTENS):
    x, y = (i % 2) * 400, (i // 2) * 430
    inner = built[key].replace(' id="', f' id="s-').replace('url(#', 'url(#s-')
    cells += (f'<g transform="translate({x},{y})">{inner}'
              f'<text x="200" y="400" text-anchor="middle" font-family="system-ui, sans-serif" '
              f'font-size="20" font-weight="600" fill="#4a3f3c">{KITTENS[key][0]}</text></g>')
with open(os.path.join(HERE, "kittens.svg"), "w") as f:
    f.write(f'{HEAD_SVG} viewBox="0 0 800 860" width="800" height="860">\n<title>Kittens</title>\n'
            f'<rect width="800" height="860" fill="#fff"/>\n{cells}\n</svg>\n')
print("wrote", ", ".join(f"svg/kitten-{k}.svg" for k in KITTENS), "and kittens.svg")
