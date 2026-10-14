"""Write the 3VOtech logo and app icon SVGs.

Usage: python3 scripts/logos.py . build/wordmarks.defs.svg

Every file is standalone: literal colors, transparent ground, the TECH wordmark as
glyph outlines (Saira at 125% width, weight 600) with the check's 54.6 degree cuts.

Every version, color included, separates the letters the same way: a knockout gap
around the V where it meets the bars and crosses the O. (Until 2026-10-13 the dark
color version blended the V and O like light instead; Steve and Dae found the color
versions muddled, delineated by color alone.)

The check's arm is the length it was first drawn. Longer arms (+10% to +30%) were
tried on 2026-10-13 and dropped the next day: they threw off the mark's balance, and
the check is meant as a hint, not a literal tick.
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

# The mark, 100 units tall: the bars of the Ǝ, the O, and the V whose left stem is
# the Ǝ's spine. Every cut is 54.6 degrees, the arm's angle (run 82 per 106 of rise).
RING = 'cx="113" cy="50" r="42" fill="none" stroke-width="20"'
BARS = ['M7.74 0H60V20H-7.74Z', 'M21.74 40H60V60H6.26Z', 'M7.74 80H60V100H-7.74Z']
V = 'M60 0H80V71.6L140 -6H166L84 100H60Z'
MARK_VB = '-12 -10 184 116'
GAP = 10  # stroke of the knockout around the V: a 3.5-unit gap after the V's own 1.5


def bars(color):
    return ''.join(f'<path d="{d}" fill="{color}" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>' for d in BARS)


def mark(kind, uid, layers=('e', 'v', 'o')):
    """The mark in its own coordinates (viewBox MARK_VB)."""
    if kind in ('light', 'dark'):
        c = LIGHT if kind == 'light' else DARK
        e, o, v = c['e'], c['o'], c['v']
    else:
        e = o = v = INKS[kind]
    out = (f'<mask id="knock-{uid}" maskUnits="userSpaceOnUse" x="-20" y="-20" width="200" height="140">'
           f'<rect x="-20" y="-20" width="200" height="140" fill="#fff"/>'
           f'<path d="{V}" fill="#000" stroke="#000" stroke-width="{GAP}" stroke-linejoin="round"/></mask>')
    knocked = ''
    if 'o' in layers:
        knocked += f'<circle {RING} stroke="{o}"/>'
    if 'e' in layers:
        knocked += bars(e)
    if knocked:
        out += f'<g mask="url(#knock-{uid})">{knocked}</g>'
    if 'v' in layers:
        out += f'<path d="{V}" fill="{v}" stroke="{v}" stroke-width="3" stroke-linejoin="round"/>'
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
    """Place the mark, scaled into the box x, y, w, h."""
    return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{MARK_VB}">{body}</svg>'


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
              nested(28, 10, 144, 92, mark(kind, 's'))
              + f'<g transform="translate(28.83 172) scale(0.03997)">{wordmark("saira", ink_of(kind), "s")}</g>',
              f'3VOtech logo, stacked, {LABEL[kind]}'))
    write(f'logos/3votech-horizontal-{sfx}.svg',
          svg('-6 -2 524 120',
              nested(0, 0, 184, 116, mark(kind, 'h'))
              + f'<g transform="translate(207.18 93.33) scale(0.09690)">{wordmark("sairaLock", ink_of(kind), "h")}</g>',
              f'3VOtech logo, horizontal, {LABEL[kind]}'))

# App icon: 1024 canvas, the mark's ink 66% of the width, centered on that ink.
# The ink spans x -9.24 to 167.5 (the arm's tip plus its stroke) and y -7.5 to 102.
left, right, top, bottom = -9.24, 167.5, -7.5, 102


def icon_mark(body, width=676):
    """Place the mark on a 1024 canvas, its ink `width` wide and centered."""
    s = width / (right - left)
    x = 512 - ((left + right) / 2 + 12) * s
    y = 512 - ((top + bottom) / 2 + 10) * s
    return nested(f'{x:.1f}', f'{y:.1f}', f'{184 * s:.1f}', f'{116 * s:.1f}', body)


for kind, ground in (('light', '#FFFFFF'), ('dark', '#0A1230')):
    write(f'app-icon/app-icon-{kind}.svg',
          svg('0 0 1024 1024', f'<rect width="1024" height="1024" fill="{ground}"/>{icon_mark(mark(kind, "i"))}',
              f'3VOtech app icon, {kind}', 1024, 1024))
# Icon Composer layers: each letter alone, the E and O already carrying their gap.
# The -dark set carries the dark colors, for the icon's dark appearance.
for kind, sfx in (('light', ''), ('dark', '-dark')):
    for layer, name in (('o', 'o-ring'), ('e', 'e-bars'), ('v', 'v-check')):
        write(f'app-icon/icon-layer-{name}{sfx}.svg',
              svg('0 0 1024 1024', icon_mark(mark(kind, f'l{layer}' + ('d' if sfx else ''), layers=(layer,))),
                  f'3VOtech app icon layer: {name}{sfx}', 1024, 1024))

# Android adaptive icon layers, on transparent 1024 canvases. The launcher shows the
# middle 72dp of a 108dp foreground (two thirds), so the ink is 44% of the canvas:
# 66% of what shows, as on iOS, and inside the 66dp circle every mask keeps.
# The ground is a color, white, set in the app's config.
ANDROID = round(1024 * 0.66 * 72 / 108)
write('app-icon/android-foreground.svg',
      svg('0 0 1024 1024', icon_mark(mark('light', 'af'), ANDROID),
          '3VOtech Android adaptive icon foreground', 1024, 1024))
# Themed icons (Android 13+) use only the alpha, so the ink color does not matter.
write('app-icon/android-monochrome.svg',
      svg('0 0 1024 1024', icon_mark(mark('white', 'am'), ANDROID),
          '3VOtech Android themed icon', 1024, 1024))
