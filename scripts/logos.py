"""Write the 3VOtech logo and app icon SVGs.

Usage: python3 scripts/logos.py . build/wordmarks.defs.svg

Every file is standalone: literal colors, transparent ground, the TECH wordmark as
glyph outlines (Saira at 125% width, weight 600) with the check's 54.6 degree cuts.
"""
import os
import re
import sys

OUT = sys.argv[1]
DEFS = open(sys.argv[2]).read()

LIGHT = dict(e='#2459F5', o='#0891B2', v='#7A3CF0', ink='#0D1530')
DARK = dict(e='#5C8DFF', o='#22D3EE', v='#A685FF', ink='#EAF0FF')
NAVY, WHITE, BLACK = '#0D1530', '#FFFFFF', '#000000'

RING = 'cx="113" cy="50" r="42" fill="none" stroke-width="20"'
BARS = ['M7.74 0H60V20H-7.74Z', 'M21.74 40H60V60H6.26Z', 'M7.74 80H60V100H-7.74Z']
V = 'M60 0H80V71.6L140 -6H166L84 100H60Z'
MARK_VB = '-12 -10 184 116'


def bars(color):
    return ''.join(f'<path d="{d}" fill="{color}" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>' for d in BARS)


def vee(color, blend=''):
    style = f' style="mix-blend-mode:{blend}"' if blend else ''
    return f'<path d="{V}" fill="{color}" stroke="{color}" stroke-width="3" stroke-linejoin="round"{style}/>'


def mark(kind, uid, layers=('e', 'v', 'o')):
    """The mark in its own coordinates (viewBox MARK_VB)."""
    if kind in ('light', 'dark'):
        c = LIGHT if kind == 'light' else DARK
        blend = 'screen' if kind == 'dark' else ''
        out = '<g style="isolation:isolate">'
        if 'o' in layers:
            out += f'<circle {RING} stroke="{c["o"]}"/>'
        if 'e' in layers:
            out += bars(c['e'])
        if 'v' in layers:
            out += vee(c['v'], blend)
            # the stem stays solid; only its edges and the arm pick up the glow on dark
            out += f'<rect x="60" y="0" width="20" height="100" fill="{c["v"]}"/>'
        return out + '</g>'
    ink = {'navy': NAVY, 'white': WHITE, 'black': BLACK}[kind]
    # one color: a knockout gap around the V so it still reads where it crosses the O
    return (f'<mask id="knock-{uid}" maskUnits="userSpaceOnUse" x="-20" y="-20" width="200" height="140">'
            f'<rect x="-20" y="-20" width="200" height="140" fill="#fff"/>'
            f'<path d="{V}" fill="#000" stroke="#000" stroke-width="10" stroke-linejoin="round"/></mask>'
            f'<g mask="url(#knock-{uid})"><circle {RING} stroke="{ink}"/>{bars(ink)}</g>{vee(ink)}')


def wordmark(name, ink, uid):
    m = re.search(rf'<mask id="cut-{name}".*?</mask><g id="w-{name}" mask="url\(#cut-{name}\)">.*?</g>', DEFS, re.S)
    if not m:
        raise SystemExit(f'wordmark {name} not found')
    w = m.group(0).replace(f'cut-{name}', f'cut-{uid}').replace(f' id="w-{name}"', '')
    return w.replace('var(--ink)', ink)


def ink_of(kind):
    return {'light': LIGHT['ink'], 'dark': DARK['ink'], 'navy': NAVY, 'white': WHITE, 'black': BLACK}[kind]


def svg(viewbox, body, title, w=None, h=None):
    size = f' width="{w}" height="{h}"' if w else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}"{size} role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(text)
    print(path, len(text))


SUFFIX = {'light': 'color', 'dark': 'color-dark', 'navy': 'navy', 'white': 'white', 'black': 'black'}
LABEL = {'light': 'color, for light grounds', 'dark': 'color, for dark grounds',
         'navy': 'one color, navy', 'white': 'one color, white', 'black': 'one color, black, for print'}

for kind in ('light', 'dark', 'navy', 'white', 'black'):
    sfx = SUFFIX[kind]
    write(f'logos/3votech-mark-{sfx}.svg',
          svg(MARK_VB, mark(kind, 'm'), f'3VOtech mark, {LABEL[kind]}'))
    write(f'logos/3votech-stacked-{sfx}.svg',
          svg('22 6 156 172',
              f'<svg x="28" y="10" width="144" height="92" viewBox="{MARK_VB}">{mark(kind, "s")}</svg>'
              f'<g transform="translate(28.83 172) scale(0.03997)">{wordmark("saira", ink_of(kind), "s")}</g>',
              f'3VOtech logo, stacked, {LABEL[kind]}'))
    write(f'logos/3votech-horizontal-{sfx}.svg',
          svg('-6 -2 524 120',
              f'<svg x="0" y="0" width="184" height="116" viewBox="{MARK_VB}">{mark(kind, "h")}</svg>'
              f'<g transform="translate(207.18 93.33) scale(0.09690)">{wordmark("sairaLock", ink_of(kind), "h")}</g>',
              f'3VOtech logo, horizontal, {LABEL[kind]}'))

# App icon: 1024 canvas, mark ink 66% of the width, centered on the ink
S = 676 / 176.7
X, Y = 512 - (79.1 + 12) * S, 512 - (47.3 + 10) * S
nest = f'x="{X:.1f}" y="{Y:.1f}" width="{184 * S:.1f}" height="{116 * S:.1f}" viewBox="{MARK_VB}"'
for kind, ground in (('light', '#FFFFFF'), ('dark', '#0A1230')):
    write(f'app-icon/app-icon-{"light" if kind == "light" else "dark"}.svg',
          svg('0 0 1024 1024', f'<rect width="1024" height="1024" fill="{ground}"/><svg {nest}>{mark(kind, "i")}</svg>',
              f'3VOtech app icon, {"light" if kind == "light" else "dark"}', 1024, 1024))
for layer, name in (('o', 'o-ring'), ('e', 'e-bars'), ('v', 'v-check')):
    write(f'app-icon/icon-layer-{name}.svg',
          svg('0 0 1024 1024', f'<svg {nest}>{mark("light", "l", layers=(layer,))}</svg>',
              f'3VOtech app icon layer: {name}', 1024, 1024))
