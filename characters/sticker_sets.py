#!/usr/bin/env python3
"""Three sticker-style sets, each drawn from shared shapes:

  hamsters  - thin clean outlines, many poses and props        -> svg/hamster-*.svg,  hamsters.svg
  critters  - fuzzy crayon look, one species each with a snack -> svg/critter-*.svg,  critters.svg
  loafcats  - one side-view loaf shape, many coat patterns     -> svg/loafcat-*.svg,  loafcats.svg

Run: python3 sticker_sets.py
"""
import html
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SVG_NS = ('<svg xmlns="http://www.w3.org/2000/svg" '
          'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"')
os.makedirs(os.path.join(HERE, "svg"), exist_ok=True)


def L(name, content, pivot=None):
    piv = f' data-pivot="{pivot[0]:.0f} {pivot[1]:.0f}"' if pivot else ""
    return (f'<g id="{name}" class="L-{name}" inkscape:groupmode="layer" '
            f'inkscape:label="{name}"{piv}>{content}</g>')


def ell(cx, cy, rx, ry):
    return f"M{cx - rx},{cy} A{rx},{ry} 0 1 0 {cx + rx},{cy} A{rx},{ry} 0 1 0 {cx - rx},{cy} Z"


class Pen:
    """Outline + clipped patches, with an id prefix and optional filters."""

    def __init__(self, prefix, ink, w, line_filter="", fill_filter=""):
        self.p, self.ink, self.w = prefix, ink, w
        self.lf = f' filter="url(#{line_filter})"' if line_filter else ""
        self.ff = f' filter="url(#{fill_filter})"' if fill_filter else ""
        self.n = 0

    def ln(self, w=None, color=None):
        return (f'fill="none" stroke="{color or self.ink}" stroke-width="{w or self.w}" '
                f'stroke-linecap="round" stroke-linejoin="round"{self.lf}')

    def shape(self, d, fill, patches="", outline=True, w=None):
        self.n += 1
        cid = f"{self.p}c{self.n}"
        s = f'<path d="{d}" fill="{fill}"{self.ff}/>'
        if patches:
            s = (f'<clipPath id="{cid}"><path d="{d}"/></clipPath>' + s
                 + f'<g clip-path="url(#{cid})">{patches}</g>')
        if outline:
            s += f'<path d="{d}" {self.ln(w)}/>'
        return s

    def oval(self, cx, cy, rx, ry, fill, patches="", rot=0, outline=True, w=None):
        s = self.shape(ell(cx, cy, rx, ry), fill, patches, outline, w)
        return f'<g transform="rotate({rot} {cx} {cy})">{s}</g>' if rot else s


def write_set(name, title, items, size, cols, cell, label_font, extra_defs="", bg="#fffdfa", label_color="#5a4f4a"):
    """items: list of (key, label, content, defs). Writes each SVG and a sheet."""
    w, h = size
    items = [(k, html.escape(lbl), c, d) for k, lbl, c, d in items]
    for key, label, content, defs in items:
        with open(os.path.join(HERE, "svg", f"{name}-{key}.svg"), "w") as f:
            f.write(f'{SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" data-character="{key}">'
                    f'<title>{label}</title><defs>{extra_defs}{defs}</defs>{content}</svg>\n')
    rows = math.ceil(len(items) / cols)
    cw, ch = cell
    cells = ""
    for i, (key, label, content, defs) in enumerate(items):
        x, y = (i % cols) * cw + (cw - w) / 2, (i // cols) * ch
        cells += (f'<g transform="translate({x:.0f},{y})">{content}'
                  f'<text x="{w / 2}" y="{h + 18}" text-anchor="middle" font-family="{label_font}" '
                  f'font-size="15" fill="{label_color}">{label}</text></g>')
    alldefs = extra_defs + "".join(d for *_, d in items)
    W, H = cols * cw, rows * ch + 10
    with open(os.path.join(HERE, f"{name}s.svg"), "w") as f:
        f.write(f'{SVG_NS} viewBox="0 0 {W} {H}" width="{W}" height="{H}"><title>{title}</title>'
                f'<defs>{alldefs}</defs><rect width="{W}" height="{H}" fill="{bg}"/>{cells}</svg>\n')


# =============================================================================
# 1. HAMSTERS - thin clean outline, 200x200
# =============================================================================
H_INK = "#2b2626"
PINK = "#f4b3b6"


def hamster(key, coat, pose="sit", eyes="open", prop="", hat="", arms="hold"):
    P = Pen(f"h-{key}-", H_INK, 3.4)
    base, belly = coat["base"], coat.get("belly", "#fffaf4")
    ear_fill = coat.get("ear", base)
    if pose == "sit":
        body = "M40,122 C36,82 62,54 100,54 C138,54 164,82 160,122 C158,152 136,166 100,166 C64,166 42,152 40,122 Z"
        pat = coat.get("sit_p", "") + f'<ellipse cx="100" cy="150" rx="46" ry="34" fill="{belly}"/>'
        ears = (P.oval(64, 64, 13, 12, ear_fill) + P.oval(136, 64, 13, 12, ear_fill)
                + f'<ellipse cx="64" cy="66" rx="6" ry="5" fill="{PINK}"/><ellipse cx="136" cy="66" rx="6" ry="5" fill="{PINK}"/>')
        if eyes == "open":
            e = f'<circle cx="82" cy="102" r="3.8" fill="{H_INK}"/><circle cx="118" cy="102" r="3.8" fill="{H_INK}"/>'
        else:
            e = f'<path d="M76,103 q6,4 12,0 M112,103 q6,4 12,0" {P.ln(2.8)}/>'
        face = (e + f'<ellipse cx="100" cy="110" rx="3" ry="2.2" fill="#e98d93"/>'
                f'<path d="M95,115 q2.5,3 5,0 q2.5,3 5,0" {P.ln(2.2)}/>'
                f'<ellipse cx="70" cy="114" rx="8" ry="4.5" fill="{PINK}" opacity=".6"/>'
                f'<ellipse cx="130" cy="114" rx="8" ry="4.5" fill="{PINK}" opacity=".6"/>')
        if arms == "hold":
            arm_s = f'<path d="M84,128 q6,9 12,1 M104,129 q6,8 12,-1" {P.ln(3)}/>'
        else:  # resting at sides
            arm_s = f'<path d="M70,130 q4,8 10,4 M130,130 q-4,8 -10,4" {P.ln(3)}/>'
        layers = [
            L("shadow", '<ellipse cx="100" cy="172" rx="56" ry="6" fill="#ece6e0"/>'),
            L("ears", ears, (100, 70)),
            L("feet", f'<ellipse cx="80" cy="166" rx="9" ry="5" fill="{PINK}"/><ellipse cx="120" cy="166" rx="9" ry="5" fill="{PINK}"/>'),
            L("body", P.shape(body, base, pat)
                      + f'<path d="M40,108 l-8,-2 M40,116 l-8,2 M160,108 l8,-2 M160,116 l8,2" {P.ln(2.2)}/>', (100, 166)),
            L("face", face, (100, 104)),
        ]
        if prop:
            layers.append(L("prop", prop(P), (100, 132)))
        layers.append(L("arms", arm_s, (100, 128)))
        if hat:
            layers.append(L("hat", hat(P), (100, 56)))
    else:  # loaf: side view, facing left
        body = "M28,150 C22,110 58,80 108,80 C156,80 178,112 176,142 C174,158 160,164 140,164 L48,164 C36,164 29,160 28,150 Z"
        pat = coat.get("loaf_p", "") + f'<ellipse cx="80" cy="168" rx="60" ry="16" fill="{belly}"/>'
        if eyes == "open":
            e = f'<circle cx="50" cy="124" r="3.6" fill="{H_INK}"/>'
        else:
            e = f'<path d="M44,125 q6,4 12,0" {P.ln(2.8)}/>'
        layers = [
            L("shadow", '<ellipse cx="102" cy="168" rx="80" ry="6" fill="#ece6e0"/>'),
            L("body", P.shape(body, base, pat), (102, 164)),
            L("ear", P.oval(70, 90, 12, 11, ear_fill) + f'<ellipse cx="70" cy="92" rx="6" ry="5" fill="{PINK}"/>', (70, 98)),
            L("face", e + f'<ellipse cx="30" cy="132" rx="3" ry="2.2" fill="#e98d93"/>'
                         f'<ellipse cx="52" cy="138" rx="8" ry="4.5" fill="{PINK}" opacity=".6"/>'
                         f'<path d="M28,138 l-8,0 M29,145 l-8,3" {P.ln(2.2)}/>', (44, 128)),
            L("feet", f'<ellipse cx="60" cy="165" rx="9" ry="4.5" fill="{PINK}"/><ellipse cx="140" cy="165" rx="9" ry="4.5" fill="{PINK}"/>'),
        ]
        if eyes == "closed":
            layers.append(L("zzz", '<text x="18" y="96" font-family="Georgia,serif" font-style="italic" font-size="18" fill="#9aa6c4">z</text>'
                                   '<text x="6" y="78" font-family="Georgia,serif" font-style="italic" font-size="12" fill="#9aa6c4">z</text>'))
        if prop:
            layers.append(L("prop", prop(P)))
    return "".join(layers)


# hamster coats
GOLD = dict(base="#f3d49a", belly="#fff6e6")
GRAY = dict(base="#d8d8dc", belly="#fbfbfd",
            sit_p='<path d="M100,52 v40" stroke="#9c9ca6" stroke-width="9" stroke-linecap="round"/>',
            loaf_p='<path d="M60,88 C100,76 140,84 170,112" fill="none" stroke="#9c9ca6" stroke-width="9" stroke-linecap="round"/>')
WHITE = dict(base="#fffdf9", belly="#fffdf9", ear="#c9c4c2")
CREAM = dict(base="#f2e2c6", belly="#fff8ee")
PANDA = dict(base="#fffdf9", belly="#fffdf9", ear="#4a4446",
             sit_p='<ellipse cx="60" cy="86" rx="22" ry="20" fill="#4a4446"/><ellipse cx="140" cy="86" rx="22" ry="20" fill="#4a4446"/>'
                   '<ellipse cx="100" cy="66" rx="16" ry="10" fill="#4a4446"/>',
             loaf_p='<ellipse cx="130" cy="96" rx="34" ry="22" fill="#4a4446"/>')
BLUE = dict(base="#c8d3e3", belly="#f6f8fc",
            sit_p='<path d="M100,52 v40" stroke="#8d9cb6" stroke-width="9" stroke-linecap="round"/>')
CINN = dict(base="#e3b38a", belly="#fff4e8", ear="#d39d74")


def strawberry(P):
    d = "M88,128 C84,140 92,156 100,160 C108,156 116,140 112,128 C106,124 94,124 88,128 Z"
    return (P.shape(d, "#ef6b72", w=2.6)
            + "".join(f'<circle cx="{x}" cy="{y}" r="1.3" fill="#ffe28a"/>' for x, y in [(95, 136), (104, 135), (99, 145), (106, 148)])
            + f'<path d="M90,128 l5,-6 l5,5 l5,-5 l5,6 Z" fill="#7cc07a" stroke="{H_INK}" stroke-width="2" stroke-linejoin="round"/>')


def cookie(P):
    return (P.oval(100, 140, 17, 15, "#e3b06d", w=2.6)
            + "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#6b4a3a"/>' for x, y in [(93, 135), (106, 138), (98, 147), (108, 146)]))


def book(P):
    return (f'<path d="M78,132 L100,138 L122,132 L122,156 L100,162 L78,156 Z" fill="#9ec5e8" stroke="{H_INK}" stroke-width="2.6" stroke-linejoin="round"/>'
            f'<path d="M100,138 V162" {P.ln(2.4)}/>'
            f'<path d="M84,141 l10,3 M84,148 l10,3 M106,144 l10,-3 M106,151 l10,-3" {P.ln(1.6, "#5a7590")}/>')


def scarf(P):
    return (f'<path d="M58,128 C80,140 120,140 142,128 L144,138 C120,150 80,150 56,138 Z" fill="#e0675f" stroke="{H_INK}" stroke-width="2.6" stroke-linejoin="round"/>'
            f'<path d="M124,140 L132,164 L120,166 L114,144 Z" fill="#e0675f" stroke="{H_INK}" stroke-width="2.6" stroke-linejoin="round"/>'
            f'<path d="M70,135 v8 M84,139 v8 M98,140 v8 M112,139 v8" {P.ln(1.8, "#b8443e")}/>')


def party_hat(P):
    return (f'<path d="M84,58 L100,14 L116,58 Z" fill="#a8d8b9" stroke="{H_INK}" stroke-width="2.8" stroke-linejoin="round"/>'
            f'<path d="M90,42 l8,-4 M94,52 l14,-6" {P.ln(2, "#f2a3b3")}/>'
            f'<circle cx="100" cy="13" r="5" fill="#f7d36b" stroke="{H_INK}" stroke-width="2.4"/>')


def flower_crown(P):
    s = ""
    for cx, col in [(76, "#f7b6c8"), (100, "#fde58a"), (124, "#bfe0f7")]:
        for a in range(5):
            t = a * 2 * math.pi / 5 - math.pi / 2
            s += f'<circle cx="{cx + 6 * math.cos(t):.1f}" cy="{58 + 6 * math.sin(t):.1f}" r="4.5" fill="{col}" stroke="{H_INK}" stroke-width="1.6"/>'
        s += f'<circle cx="{cx}" cy="58" r="3" fill="#f2a14a"/>'
    return s


def seed_bag(P):  # loaf hugging a sunflower-seed pouch
    return (f'<path d="M150,128 C150,112 164,104 178,108 C190,112 192,128 186,142 L152,148 Z" fill="#e8d3a8" stroke="{H_INK}" stroke-width="2.6" stroke-linejoin="round"/>'
            f'<path d="M160,112 l8,-8 l6,8" {P.ln(2.2)}/>')


HAMSTERS = [
    ("strawberry", "Strawberry snack", GOLD, dict(prop=strawberry)),
    ("cookie", "Cookie time", GRAY, dict(prop=cookie)),
    ("reader", "Little reader", CREAM, dict(prop=book)),
    ("party", "Party hat", PANDA, dict(hat=party_hat, arms="side")),
    ("winter", "Winter scarf", BLUE, dict(hat=scarf, arms="side")),
    ("flowers", "Flower crown", CINN, dict(hat=flower_crown, arms="side")),
    ("nap", "Nap time", WHITE, dict(pose="loaf", eyes="closed")),
    ("loaf", "Loaf mode", GRAY, dict(pose="loaf")),
    ("snacker", "Seed stash", GOLD, dict(pose="loaf", prop=seed_bag)),
    ("sleepy", "Sleepy", PANDA, dict(eyes="closed", arms="side")),
]
items = [(k, lbl, hamster(k, coat, **kw), "") for k, lbl, coat, kw in HAMSTERS]
write_set("hamster", "Hamsters", items, (200, 190), 5, (210, 230), "system-ui, sans-serif")


# =============================================================================
# 2. FUZZY CRITTERS - crayon look, 240x240
# =============================================================================
C_INK = "#4d4242"
FUZZ_DEFS = ('<filter id="fz-line" x="-10%" y="-10%" width="120%" height="120%">'
             '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="3" result="n"/>'
             '<feDisplacementMap in="SourceGraphic" in2="n" scale="5"/><feGaussianBlur stdDeviation=".5"/></filter>'
             '<filter id="fz-fill" x="-10%" y="-10%" width="120%" height="120%">'
             '<feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="1" seed="7" result="n"/>'
             '<feDisplacementMap in="SourceGraphic" in2="n" scale="6"/></filter>'
             '<filter id="fz-soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>')


def blush(cx1, cx2, cy, r=11):
    return (f'<g filter="url(#fz-soft)"><circle cx="{cx1}" cy="{cy}" r="{r}" fill="#f59ca4" opacity=".7"/>'
            f'<circle cx="{cx2}" cy="{cy}" r="{r}" fill="#f59ca4" opacity=".7"/></g>')


def dot_eyes(P, y=112, dx=26, r=6.5, col=C_INK):
    return "".join(f'<circle cx="{120 + s * dx}" cy="{y}" r="{r}" fill="{col}"/>'
                   f'<circle cx="{120 + s * dx + 2}" cy="{y - 2.5}" r="2" fill="#fff"/>' for s in (-1, 1))


def critter_base(P, fur, ears, face, prop="", body_p="", head_p="", arms_fill=None, feet_fill=None, tail=""):
    arms_fill = arms_fill or fur
    feet_fill = feet_fill or fur
    return "".join([
        L("shadow", '<ellipse cx="120" cy="222" rx="70" ry="7" fill="#efe9ef"/>'),
        L("tail", tail, (160, 200)) if tail else "",
        L("ears", ears, (120, 70)),
        L("body", P.oval(120, 178, 54, 42, fur, body_p), (120, 220)),
        L("feet", P.oval(94, 212, 17, 12, feet_fill) + P.oval(146, 212, 17, 12, feet_fill), (120, 212)),
        L("head", P.oval(120, 108, 70, 58, fur, head_p), (120, 160)),
        L("face", face, (120, 112)),
        L("prop", prop, (120, 172)) if prop else "",
        L("arms", P.oval(96, 172, 13, 15, arms_fill, rot=-25) + P.oval(144, 172, 13, 15, arms_fill, rot=25), (120, 168)),
    ])


def critters():
    out = []

    def pen(k):
        return Pen(f"cr-{k}-", C_INK, 4.6, "fz-line", "fz-fill")

    # panda with an onigiri
    P = pen("panda")
    BLK = "#5a5254"
    face = (P.oval(92, 112, 15, 19, BLK, rot=25, outline=False) + P.oval(148, 112, 15, 19, BLK, rot=-25, outline=False)
            + "".join(f'<circle cx="{x}" cy="112" r="5" fill="#fff"/>' for x in (94, 146))
            + f'<ellipse cx="120" cy="128" rx="5" ry="3.5" fill="{C_INK}"/>' + blush(78, 162, 136))
    oni = (P.shape("M120,150 L142,186 L98,186 Z", "#fffdf7", w=3.6)
           + f'<rect x="108" y="172" width="24" height="14" fill="#3f4a44"/>')
    out.append(("panda", "Panda & onigiri", critter_base(
        P, "#fffdf8", P.oval(70, 64, 20, 18, BLK) + P.oval(170, 64, 20, 18, BLK), face, oni,
        arms_fill=BLK, feet_fill=BLK), ""))

    # bunny with a carrot
    P = pen("bunny")
    ears = (P.oval(94, 46, 15, 40, "#fff7f6", f'<ellipse cx="94" cy="46" rx="7" ry="28" fill="#f6c2c8"/>', rot=-12)
            + P.oval(146, 46, 15, 40, "#fff7f6", f'<ellipse cx="146" cy="46" rx="7" ry="28" fill="#f6c2c8"/>', rot=12))
    face = dot_eyes(P) + f'<path d="M116,126 l4,3 l4,-3" {P.ln(3)}/>' + blush(80, 160, 132)
    carrot = (P.shape("M108,160 L132,160 L120,196 Z", "#f39a4a", w=3.6)
              + f'<path d="M114,158 l-6,-12 M120,158 v-14 M126,158 l6,-12" stroke="#7cc07a" stroke-width="6" stroke-linecap="round"/>')
    out.append(("bunny", "Bunny & carrot", critter_base(P, "#fff7f6", ears, face, carrot), ""))

    # penguin with a fish
    P = pen("penguin")
    face = (P.shape("M78,110 C78,84 100,78 120,92 C140,78 162,84 162,110 C162,140 140,152 120,152 C100,152 78,140 78,110 Z",
                    "#ffffff", outline=False)
            + dot_eyes(P, y=114, dx=22) + P.shape("M112,126 L128,126 L120,136 Z", "#f4a55a", w=3) + blush(86, 154, 134, 9))
    fish = (P.oval(120, 178, 22, 11, "#8fc1e8", w=3.4) + P.shape("M140,178 L156,168 L156,188 Z", "#8fc1e8", w=3.4)
            + f'<circle cx="108" cy="175" r="2.6" fill="{C_INK}"/>')
    out.append(("penguin", "Penguin & fish", critter_base(
        P, "#8e9298", "", face, fish, body_p='<ellipse cx="120" cy="190" rx="38" ry="34" fill="#ffffff"/>',
        feet_fill="#f4a55a"), ""))

    # koala with a leaf
    P = pen("koala")
    ears = (P.oval(58, 84, 30, 28, "#b9b8bf", '<ellipse cx="62" cy="86" rx="16" ry="15" fill="#f6f1f2"/>')
            + P.oval(182, 84, 30, 28, "#b9b8bf", '<ellipse cx="178" cy="86" rx="16" ry="15" fill="#f6f1f2"/>'))
    face = (dot_eyes(P, y=106, dx=30, r=6) + P.oval(120, 124, 13, 15, "#4d4446", outline=False) + blush(78, 162, 132))
    leaf = (P.shape("M100,190 C100,164 124,150 144,154 C146,176 128,194 100,190 Z", "#8cc98a", w=3.4)
            + f'<path d="M104,186 C114,176 126,166 140,158" {P.ln(2.4, "#4f8a55")}/>')
    out.append(("koala", "Koala & leaf", critter_base(P, "#b9b8bf", ears, face, leaf,
                                                     body_p='<ellipse cx="120" cy="196" rx="30" ry="22" fill="#f6f1f2"/>'), ""))

    # red panda with tea
    P = pen("redpanda")
    RP, BR = "#e7875a", "#6e4436"
    ears = (P.shape("M62,92 L70,40 L104,62 Z", RP, '<path d="M72,80 L76,52 L96,66 Z" fill="#fff4ea"/>')
            + P.shape("M178,92 L170,40 L136,62 Z", RP, '<path d="M168,80 L164,52 L144,66 Z" fill="#fff4ea"/>'))
    face = (dot_eyes(P, y=112) + f'<ellipse cx="120" cy="128" rx="5" ry="3.5" fill="{C_INK}"/>')
    head_p = ('<ellipse cx="120" cy="138" rx="30" ry="18" fill="#fff4ea"/>'
              '<ellipse cx="92" cy="96" rx="10" ry="6" fill="#fff4ea"/><ellipse cx="148" cy="96" rx="10" ry="6" fill="#fff4ea"/>')
    tea = (P.shape("M102,162 L138,162 L134,192 C130,198 110,198 106,192 Z", "#fdfbf7", w=3.4)
           + f'<path d="M138,170 C150,170 150,184 136,184" {P.ln(3.4)}/>'
           + f'<path d="M112,154 q-4,-8 0,-14 M126,154 q-4,-8 0,-14" {P.ln(2.4, "#c8bfc4")}/>')
    tail = (P.oval(172, 196, 34, 16, RP, ''.join(f'<rect x="{x}" y="170" width="10" height="60" fill="{BR}"/>' for x in (160, 182)),
                   rot=-30))
    out.append(("redpanda", "Red panda & tea", critter_base(
        P, RP, ears, face, tea, head_p=head_p, body_p=f'<rect x="60" y="180" width="120" height="60" fill="{BR}"/>',
        arms_fill=BR, feet_fill=BR, tail=tail), ""))

    # frog with a flower
    P = pen("frog")
    G = "#a6d68c"
    ears = (P.oval(88, 66, 22, 20, G) + P.oval(152, 66, 22, 20, G)
            + "".join(f'<circle cx="{x}" cy="66" r="7" fill="{C_INK}"/><circle cx="{x + 2}" cy="63" r="2.2" fill="#fff"/>' for x in (88, 152)))
    face = (f'<path d="M96,122 Q120,140 144,122" {P.ln(3.4)}/>' + blush(78, 162, 124))
    flower = ("".join(f'<circle cx="{120 + 9 * math.cos(a):.1f}" cy="{168 + 9 * math.sin(a):.1f}" r="7.5" fill="#f7b6c8" '
                      f'stroke="{C_INK}" stroke-width="2.6"/>' for a in [i * 2 * math.pi / 5 for i in range(5)])
              + f'<circle cx="120" cy="168" r="5.5" fill="#fde58a"/>'
              + f'<path d="M120,178 v24" stroke="#5fa35f" stroke-width="5" stroke-linecap="round"/>')
    out.append(("frog", "Frog & flower", critter_base(P, G, ears, face, flower,
                                                     body_p='<ellipse cx="120" cy="194" rx="32" ry="24" fill="#e6f4cf"/>'), ""))

    # sheep with a star
    P = pen("sheep")
    W = "#fbf7ee"
    wool = "".join(P.oval(120 + 62 * math.cos(a), 104 + 50 * math.sin(a), 18, 18, W, outline=True)
                   for a in [i * 2 * math.pi / 14 for i in range(14)])
    ears = wool + P.oval(54, 112, 18, 9, "#e8c7a8", rot=20) + P.oval(186, 112, 18, 9, "#e8c7a8", rot=-20)
    face = (P.oval(120, 116, 44, 38, "#f1dcc4", outline=False) + dot_eyes(P, y=114, dx=20, r=5.5)
            + f'<path d="M115,128 q5,4 10,0" {P.ln(2.8)}/>' + blush(92, 148, 130, 8))
    star = (P.shape("M120,152 L126,166 L141,167 L129,177 L133,192 L120,183 L107,192 L111,177 L99,167 L114,166 Z", "#fde58a", w=3.2))
    out.append(("sheep", "Sheep & star", critter_base(P, W, ears, face, star, feet_fill="#8a6f60", arms_fill=W), ""))

    # tiger with ice cream
    P = pen("tiger")
    T = "#f4b36a"
    ears = (P.oval(70, 64, 20, 18, T, '<ellipse cx="70" cy="66" rx="10" ry="9" fill="#fff1de"/>')
            + P.oval(170, 64, 20, 18, T, '<ellipse cx="170" cy="66" rx="10" ry="9" fill="#fff1de"/>'))
    stripes = (f'<path d="M110,52 l4,16 M120,50 v18 M130,52 l-4,16 M52,100 l18,4 M52,114 l16,0 M188,100 l-18,4 M188,114 l-16,0" '
               f'stroke="#9a5a33" stroke-width="5" stroke-linecap="round"/>')
    face = dot_eyes(P) + f'<ellipse cx="120" cy="126" rx="5" ry="3.5" fill="{C_INK}"/>' + blush(80, 160, 134)
    ice = (P.shape("M108,176 L132,176 L120,204 Z", "#e8bf84", w=3.2)
           + P.oval(120, 166, 15, 13, "#f7b6c8", w=3.2) + P.oval(120, 150, 12, 11, "#fff3d6", w=3.2))
    out.append(("tiger", "Tiger & ice cream", critter_base(
        P, T, ears, face, ice, head_p=stripes + '<ellipse cx="120" cy="134" rx="32" ry="18" fill="#fff1de"/>',
        body_p='<ellipse cx="120" cy="196" rx="30" ry="22" fill="#fff1de"/>'), ""))
    return out


write_set("critter", "Fuzzy critters", critters(), (240, 235), 4, (250, 270), "system-ui, sans-serif",
          extra_defs=FUZZ_DEFS)


# =============================================================================
# 3. LOAF CATS - one side-view shape, many coats, 220x170
# =============================================================================
K_INK = "#1f1c1c"
LOAF = ("M34,152 C24,142 22,102 30,76 L36,36 L60,54 C72,51 86,51 96,54 L116,36 L118,76 "
        "C150,76 176,98 178,128 C180,146 170,152 152,152 Z")
TAIL_D = "M148,142 h46 a10,10 0 0 1 0,20 h-46 Z"


def loafcat(key, base, patches="", tail_fill=None, tail_p="", eye=K_INK):
    P = Pen(f"lc-{key}-", K_INK, 4.6)
    return "".join([
        L("shadow", '<ellipse cx="112" cy="160" rx="96" ry="6" fill="#ece8e2"/>'),
        L("tail", P.shape(TAIL_D, tail_fill or base, tail_p), (150, 152)),
        L("body", P.shape(LOAF, base, patches)
                  + f'<path d="M88,152 v-16 M124,152 C120,130 136,118 156,122" {P.ln(3.6)}/>', (100, 152)),
        L("face", f'<ellipse cx="56" cy="98" rx="2.6" ry="4.6" fill="{eye}"/>'
                  f'<ellipse cx="82" cy="98" rx="2.6" ry="4.6" fill="{eye}"/>'
                  f'<path d="M66,104 h4" {P.ln(2.4)}/>'
                  f'<path d="M24,98 h-8 M24,106 l-8,2" {P.ln(2.4)}/>', (69, 100)),
    ])


def stripes_on(color, xs, y0=60, y1=150, w=7):
    return "".join(f'<path d="M{x},{y0} l-6,{y1 - y0}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>' for x in xs)


ORANGE, OR_DK, BLACK, GREY, CREAMC, WHITEC = "#f4c27a", "#d98a3c", "#3d393a", "#b9b9bd", "#f6ead2", "#fffdf9"
LOAFCATS = [
    ("snow", "Snow (white)", WHITEC, "", None, ""),
    ("calico", "Calico", WHITEC,
     f'<ellipse cx="40" cy="50" rx="26" ry="22" fill="{BLACK}"/><ellipse cx="150" cy="110" rx="40" ry="34" fill="{ORANGE}"/>'
     f'<ellipse cx="108" cy="58" rx="16" ry="14" fill="{ORANGE}"/>', BLACK, f'<rect x="170" y="140" width="40" height="30" fill="{ORANGE}"/>'),
    ("marmalade", "Marmalade tabby", ORANGE,
     stripes_on(OR_DK, [136, 154, 170], 80) + f'<path d="M58,62 l2,12 M70,58 v14 M82,62 l-2,12" stroke="{OR_DK}" stroke-width="5" stroke-linecap="round"/>',
     None, stripes_on(OR_DK, [168, 184, 200], 140, 165, 7)),
    ("ash", "Ash (gray)", GREY, "", None, ""),
    ("midnight", "Midnight (black)", BLACK, "", None, "", "#f2c14e"),
    ("tuxedo", "Tuxedo", BLACK,
     f'<ellipse cx="66" cy="146" rx="30" ry="26" fill="{WHITEC}"/>', None,
     f'<rect x="186" y="140" width="30" height="30" fill="{WHITEC}"/>'),
    ("pointed", "Pointed (cream)", CREAMC,
     f'<ellipse cx="69" cy="104" rx="26" ry="20" fill="#8a7468" opacity=".85"/>'
     f'<path d="M30,30 L60,56 L36,70 Z M120,30 L96,56 L118,70 Z" fill="#8a7468"/>', "#8a7468", ""),
    ("peach", "Peach patch", WHITEC,
     f'<ellipse cx="100" cy="50" rx="24" ry="22" fill="{ORANGE}"/><ellipse cx="160" cy="130" rx="22" ry="18" fill="{ORANGE}"/>',
     ORANGE, ""),
    ("silver", "Silver tabby", "#d9d9dd", stripes_on("#9b9ba3", [134, 150, 166], 80), None,
     stripes_on("#9b9ba3", [166, 182, 198], 140, 165, 7)),
    ("blue", "Blue", "#8f9ab8", "", None, ""),
    ("tortie", "Tortie", "#4a3a34",
     f'<ellipse cx="44" cy="60" rx="22" ry="22" fill="{OR_DK}"/><ellipse cx="140" cy="96" rx="30" ry="22" fill="{OR_DK}"/>'
     f'<ellipse cx="160" cy="140" rx="20" ry="12" fill="#e7a35e"/>', OR_DK, ""),
    ("tabbywhite", "Brown tabby & white", "#a3907b",
     stripes_on("#6f5f50", [134, 150, 166], 80)
     + f'<ellipse cx="66" cy="146" rx="30" ry="26" fill="{WHITEC}"/>', None,
     stripes_on("#6f5f50", [166, 182, 198], 140, 165, 7)),
]
items = []
for row in LOAFCATS:
    key, label, base, pats, tail_fill, tail_p = row[:6]
    eye = row[6] if len(row) > 6 else K_INK
    items.append((key, label, loafcat(key, base, pats, tail_fill, tail_p, eye), ""))
write_set("loafcat", "Loaf cats", items, (220, 170), 4, (230, 205), "system-ui, sans-serif")

print("wrote hamsters.svg, critters.svg, loafcats.svg and their per-character SVGs")
