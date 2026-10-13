"""Write the 3VOtech logo and app icon SVGs.

Usage: python3 scripts/logos.py . build/wordmarks.defs.svg

Every file is standalone: literal colors, transparent ground, the TECH wordmark as
glyph outlines (Saira at 125% width, weight 600) with the check's 54.6 degree cuts.

Every version, color included, separates the letters the same way: a knockout gap
around the V where it meets the bars and crosses the O. (Until 2026-10-13 the dark
color version blended the V and O like light instead; Steve and Dae found the color
versions muddled, delineated by color alone.)
"""
import os
import re
import sys

OUT = sys.argv[1]
DEFS = open(sys.argv[2]).read()

LIGHT = dict(e='#2459F5', o='#0891B2', v='#7A3CF0', ink='#0D1530')
DARK = dict(e='#5C8DFF', o='#22D3EE', v='#A685FF', ink='#EAF0FF')
NAVY, WHITE, BLACK = '#0D1530', '#FFFFFF', '#000000'
INKS = {'navy': NAVY, 'white': WHITE, 'black': BLACK}

# How far the check's arm extends past its original top, as a share of its rise.
# Subtle on purpose: the mark and stacked logo +10%, the horizontal logo +15%,
# where TECH balances it. +30% was tried and tipped the mark's weight up and right.
ARM_MARK = 0.10
ARM_HORIZONTAL = 0.15

# The mark, 100 units tall: the bars of the Ǝ, the O, and the V whose left stem is
# the Ǝ's spine. Every cut is 54.6 degrees, the arm's angle (run 82 per 106 of rise).
RING = 'cx="113" cy="50" r="42" fill="none" stroke-width="20"'
BARS = ['M7.74 0H60V20H-7.74Z', 'M21.74 40H60V60H6.26Z', 'M7.74 80H60V100H-7.74Z']
BASE_VB = '-12 -10 184 116'  # the mark's frame before any arm extension; layouts place it by this
GAP = 10  # stroke of the knockout around the V: a 3.5-unit gap after the V's own 1.5


def vee(arm):
    """The V. The arm grows along its own line; the stem and the inner corner stay put."""
    return f'M60 0H80V71.6L{140 + 82 * arm:.1f} {-6 - 106 * arm:.1f}H{166 + 82 * arm:.1f}L84 100H60Z'


def arm_top(arm):
    """The topmost ink of the mark, in mark units: the arm's tip plus its stroke."""
    return -6 - 106 * arm - 1.5


def bars(color):
    return ''.join(f'<path d="{d}" fill="{color}" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>' for d in BARS)


def mark(kind, uid, arm, layers=('e', 'v', 'o')):
    """The mark in its own coordinates (BASE_VB, with the arm free to rise above it)."""
    if kind in ('light', 'dark'):
        c = LIGHT if kind == 'light' else DARK
        e, o, v = c['e'], c['o'], c['v']
    else:
        e = o = v = INKS[kind]
    path = vee(arm)
    out = (f'<mask id="knock-{uid}" maskUnits="userSpaceOnUse" x="-30" y="-60" width="260" height="180">'
           f'<rect x="-30" y="-60" width="260" height="180" fill="#fff"/>'
           f'<path d="{path}" fill="#000" stroke="#000" stroke-width="{GAP}" stroke-linejoin="round"/></mask>')
    knocked = ''
    if 'o' in layers:
        knocked += f'<circle {RING} stroke="{o}"/>'
    if 'e' in layers:
        knocked += bars(e)
    if knocked:
        out += f'<g mask="url(#knock-{uid})">{knocked}</g>'
    if 'v' in layers:
        out += f'<path d="{path}" fill="{v}" stroke="{v}" stroke-width="3" stroke-linejoin="round"/>'
    return out


def wordmark(name, ink, uid):
    m = re.search(rf'<mask id="cut-{name}".*?</mask><g id="w-{name}" mask="url\(#cut-{name}\)">.*?</g>', DEFS, re.S)
    if not m:
        raise SystemExit(f'wordmark {name} not found')
    w = m.group(0).replace(f'cut-{name}', f'cut-{uid}').replace(f' id="w-{name}"', '')
    return w.replace('var(--ink)', ink)


def ink_of(kind):
    return {'light': LIGHT['ink'], 'dark': DARK['ink'], **INKS}[kind]


def svg(viewbox, body, title, w=None, h=None):
    size = f' width="{w}" height="{h}"' if w else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}"{size} role="img" aria-label="{title}">'
            f'<title>{title}</title>{body}</svg>\n')


def nested(x, y, w, h, body):
    """Place the mark by its base frame; overflow lets the longer arm rise past it."""
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{BASE_VB}" overflow="visible">{body}</svg>'


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(text)
    print(path, len(text))


SUFFIX = {'light': 'color', 'dark': 'color-dark', 'navy': 'navy', 'white': 'white', 'black': 'black'}
LABEL = {'light': 'color, for light grounds', 'dark': 'color, for dark grounds',
         'navy': 'one color, navy', 'white': 'one color, white', 'black': 'one color, black, for print'}

# Frames: the mark alone keeps 4 units above the arm's tip; the stacked logo places the
# mark at 144/184 scale, the horizontal at 1:1, so their tops follow the arm the same way.
mark_top = int(arm_top(ARM_MARK) - 4)
MARK_VB = f'-12 {mark_top} {184 + round(82 * ARM_MARK)} {106 - mark_top}'
STACK_SCALE = 144 / 184
stack_top = int(10 + (arm_top(ARM_MARK) + 10) * STACK_SCALE - 4)
HZ_TOP = int(arm_top(ARM_HORIZONTAL) + 10 - 3)

for kind in ('light', 'dark', 'navy', 'white', 'black'):
    sfx = SUFFIX[kind]
    write(f'logos/3votech-mark-{sfx}.svg',
          svg(MARK_VB, mark(kind, 'm', ARM_MARK), f'3VOtech mark, {LABEL[kind]}'))
    write(f'logos/3votech-stacked-{sfx}.svg',
          svg(f'22 {stack_top} 156 {178 - stack_top}',
              nested(28, 10, 144, 92, mark(kind, 's', ARM_MARK))
              + f'<g transform="translate(28.83 172) scale(0.03997)">{wordmark("saira", ink_of(kind), "s")}</g>',
              f'3VOtech logo, stacked, {LABEL[kind]}'))
    # TECH stays put: the longer arm rises above the cap line and never reaches the T
    write(f'logos/3votech-horizontal-{sfx}.svg',
          svg(f'-6 {HZ_TOP} 524 {118 - HZ_TOP}',
              nested(0, 0, 184, 116, mark(kind, 'h', ARM_HORIZONTAL))
              + f'<g transform="translate(207.18 93.33) scale(0.09690)">{wordmark("sairaLock", ink_of(kind), "h")}</g>',
              f'3VOtech logo, horizontal, {LABEL[kind]}'))

# App icon: 1024 canvas, the mark's ink 66% of the width, centered on that ink.
left, right = -9.24, 166 + 82 * ARM_MARK + 1.5
top, bottom = arm_top(ARM_MARK), 102
S = 676 / (right - left)
X = 512 - ((left + right) / 2 + 12) * S
Y = 512 - ((top + bottom) / 2 + 10) * S


def icon_mark(body):
    return nested(f'{X:.1f}', f'{Y:.1f}', f'{184 * S:.1f}', f'{116 * S:.1f}', body)


for kind, ground in (('light', '#FFFFFF'), ('dark', '#0A1230')):
    write(f'app-icon/app-icon-{kind}.svg',
          svg('0 0 1024 1024', f'<rect width="1024" height="1024" fill="{ground}"/>{icon_mark(mark(kind, "i", ARM_MARK))}',
              f'3VOtech app icon, {kind}', 1024, 1024))
# Icon Composer layers: each letter alone, the E and O already carrying their gap
for layer, name in (('o', 'o-ring'), ('e', 'e-bars'), ('v', 'v-check')):
    write(f'app-icon/icon-layer-{name}.svg',
          svg('0 0 1024 1024', icon_mark(mark('light', f'l{layer}', ARM_MARK, layers=(layer,))),
              f'3VOtech app icon layer: {name}', 1024, 1024))
