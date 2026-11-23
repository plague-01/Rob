#!/usr/bin/env python3
"""Fluffy little bears: one fuzzy silhouette (head, ears, arms, legs) traced as a chain
of small bumps, dot eyes, a tiny nose and soft blush.

Writes svg/fluffy-<name>.svg (layered, 320x300) and fluffy-bears.svg (sheet).
Run: python3 fluffy_bears.py
"""
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#4b2a24"
HEAD_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"')

# Silhouette traced clockwise: left ear, head top, right ear, right arm, legs, left arm.
OUTLINE = [
    (70, 88), (57, 64), (64, 40), (86, 28), (108, 34), (118, 50),
    (126, 62), (142, 58), (159, 56), (176, 58), (192, 62),
    (200, 50), (210, 34), (232, 28), (254, 40), (261, 64), (248, 88),
    (253, 104), (254, 128), (249, 150), (238, 168),
    (234, 176), (248, 181), (256, 193), (249, 205), (233, 207),
    (228, 222), (229, 240),
    (227, 252), (214, 263), (196, 261), (188, 250),
    (159, 247),
    (130, 250), (122, 261), (104, 263), (91, 252),
    (89, 240), (90, 222),
    (85, 207), (69, 205), (62, 193), (70, 181), (84, 176),
    (80, 168), (69, 150), (64, 128), (65, 104),
]


def fuzzy_path(points, seed, step=17):
    """Close the outline with small outward bumps (clockwise order + sweep=1 bulges outward)."""
    rnd = random.Random(seed)
    pts = []
    n = len(points)
    for i in range(n):
        (x1, y1), (x2, y2) = points[i], points[(i + 1) % n]
        seg = math.hypot(x2 - x1, y2 - y1)
        parts = max(1, round(seg / step))
        for j in range(parts):
            t = j / parts
            pts.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * t))
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        r = math.hypot(x2 - x1, y2 - y1) * rnd.uniform(.56, .7)
        d += f" A{r:.1f},{r:.1f} 0 0 1 {x2:.1f},{y2:.1f}"
    return d + " Z"


def L(name, content, pivot=None):
    piv = f' data-pivot="{pivot[0]} {pivot[1]}"' if pivot else ""
    return (f'<g id="{name}" class="L-{name}" inkscape:groupmode="layer" '
            f'inkscape:label="{name}"{piv}>\n{content}\n</g>')


def defs(p):
    return (f'<filter id="{p}wobble" x="-5%" y="-5%" width="110%" height="110%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" seed="5"/>'
            f'<feDisplacementMap in="SourceGraphic" scale="2.4"/></filter>'
            f'<filter id="{p}soft" x="-50%" y="-50%" width="200%" height="200%">'
            f'<feGaussianBlur stdDeviation="4.5"/></filter>')


def line(p, w=3.4, color=INK):
    return (f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" filter="url(#{p}wobble)"')


def bear(key, fur, seed, eyes="open", accessory=""):
    p = key + "-"
    d = fuzzy_path(OUTLINE, seed)
    if eyes == "open":
        e = (f'<ellipse cx="129" cy="128" rx="6.5" ry="7.5" fill="{INK}"/>'
             f'<ellipse cx="189" cy="128" rx="6.5" ry="7.5" fill="{INK}"/>'
             f'<circle cx="131" cy="125" r="1.8" fill="#fff"/><circle cx="191" cy="125" r="1.8" fill="#fff"/>')
    else:
        e = f'<path d="M121,129 q8,6 16,0 M181,129 q8,6 16,0" {line(p, 3.6)}/>'
    return "\n".join([
        L("shadow", '<ellipse cx="159" cy="270" rx="78" ry="7" fill="#e7dfe6"/>'),
        L("body", f'<path d="{d}" fill="{fur}"/>'
                  f'<path d="{d}" {line(p, 6.5)}/>'
                  # faint arm creases, like a soft plush seam
                  f'<path d="M98,178 q8,6 18,4 M222,178 q-8,6 -18,4" {line(p, 2.6, "#00000033")}/>', (159, 262)),
        L("blush", f'<g filter="url(#{p}soft)"><circle cx="110" cy="142" r="13" fill="#f39a9a" opacity=".55"/>'
                   f'<circle cx="208" cy="142" r="13" fill="#f39a9a" opacity=".55"/></g>'),
        L("eyes", e, (159, 128)),
        L("nose", f'<ellipse cx="159" cy="134" rx="2.6" ry="2" fill="{INK}"/>', (159, 134)),
        L("mouth", f'<path d="M152,142 q3.5,3 7,0 q3.5,3 7,0" {line(p, 2.2, "#8a5a4e")}/>', (159, 142)),
        *( [L("accessory", accessory)] if accessory else [] ),
    ])


HEART = ('<path d="M159,206 C150,196 136,198 136,210 C136,222 152,230 159,238 '
         'C166,230 182,222 182,210 C182,198 168,196 159,206 Z" fill="#ef6f7b" stroke="#4b2a24" '
         'stroke-width="3.2" stroke-linejoin="round" filter="url(#honey-wobble)"/>'
         '<ellipse cx="148" cy="208" rx="4" ry="2.6" fill="#fff" opacity=".7"/>')
BOW = ('<g transform="rotate(-14 236 58)" filter="url(#cocoa-wobble)">'
       '<path d="M236,58 L214,44 L214,72 Z" fill="#9fc4e8" stroke="#4b2a24" stroke-width="3" stroke-linejoin="round"/>'
       '<path d="M236,58 L258,44 L258,72 Z" fill="#9fc4e8" stroke="#4b2a24" stroke-width="3" stroke-linejoin="round"/>'
       '<circle cx="236" cy="58" r="6.5" fill="#c3dbf2" stroke="#4b2a24" stroke-width="3"/></g>')
FLOWER = ('<g filter="url(#lilac-wobble)">'
          + "".join(f'<circle cx="{88 + 9 * math.cos(a):.1f}" cy="{52 + 9 * math.sin(a):.1f}" r="7" '
                    f'fill="#fff6a8" stroke="#4b2a24" stroke-width="2.6"/>'
                    for a in [i * 2 * math.pi / 5 - math.pi / 2 for i in range(5)])
          + '<circle cx="88" cy="52" r="5" fill="#f5b04c" stroke="#4b2a24" stroke-width="2.6"/></g>')
ZZZ = ('<text x="236" y="70" font-family="Georgia, serif" font-style="italic" font-size="22" fill="#9bb7a8">z</text>'
       '<text x="254" y="48" font-family="Georgia, serif" font-style="italic" font-size="15" fill="#9bb7a8">z</text>')

BEARS = {
    "honey": ("Honey (holding a heart)", "#f8d9a6", 3, "open", HEART),
    "cocoa": ("Cocoa (blue bow)", "#d4ab8e", 8, "open", BOW),
    "lilac": ("Lilac (flower clip)", "#e4dbf4", 13, "open", FLOWER),
    "mint": ("Mint (sleepy)", "#d4eedf", 21, "closed", ZZZ),
}

os.makedirs(os.path.join(HERE, "svg"), exist_ok=True)
built = {}
for key, (title, fur, seed, eyes, acc) in BEARS.items():
    content = bear(key, fur, seed, eyes, acc)
    built[key] = content
    with open(os.path.join(HERE, "svg", f"fluffy-{key}.svg"), "w") as f:
        f.write(f'{HEAD_SVG} viewBox="0 0 320 300" width="320" height="300" data-character="{key}">\n'
                f'<title>{title}</title>\n<defs>{defs(key + "-")}</defs>\n{content}\n</svg>\n')

cells = ""
for i, key in enumerate(BEARS):
    x, y = (i % 2) * 330, (i // 2) * 330
    cells += (f'<g transform="translate({x + 10},{y})">{built[key]}'
              f'<text x="159" y="310" text-anchor="middle" font-family="Georgia, serif" font-size="17" '
              f'fill="#6b4a42">{BEARS[key][0]}</text></g>')
with open(os.path.join(HERE, "fluffy-bears.svg"), "w") as f:
    f.write(f'{HEAD_SVG} viewBox="0 0 670 660" width="670" height="660">\n<title>Fluffy bears</title>\n'
            f'<defs>{"".join(defs(k + "-") for k in BEARS)}</defs>\n'
            f'<rect width="670" height="660" fill="#fffdfb"/>\n{cells}\n</svg>\n')
print("wrote", ", ".join(f"svg/fluffy-{k}.svg" for k in BEARS), "and fluffy-bears.svg")
