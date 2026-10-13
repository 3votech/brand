"""Build the TECH wordmarks as glyph outlines.

Saira at 125% width and weight 600 (Saira Expanded), in capitals. Every place a
horizontal stroke ends gets the logo's cut: 54.6 degrees from horizontal, parallel
to the check mark's arm (run 82 per 106 of rise). The cuts are masks, so the
glyphs stay exactly as Saira draws them.

Writes build/wordmarks.defs.svg: one <mask> and one <g id="w-NAME"> per wordmark,
in font units (y up is negative), filled with var(--ink).

  saira      tracked to the mark's width, for the stacked logo
  sairaLock  tracking 110, for the horizontal logo
"""

import os

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

SLOPE = 82 / 106  # the check's arm: run per unit of rise
MARK_L, MARK_R = 30, 168  # the mark's ink in the stacked layout, in its units

# Where each glyph's horizontal strokes end, in glyph-local font units:
# (side, x, y_top, y_bottom). R: the cut keeps the top corner; L: the bottom one.
SAIRA_CUTS = {
    'T': [('L', 29.15, -688, -570.91), ('R', 652.96, -688, -570.91)],
    'E': [('R', 646.79, -688, -575.10), ('R', 589.21, -402.75, -290.51), ('R', 646.79, -112.90, 0)],
    'C': [('R', 608.58, -678.60, -571.70), ('R', 613.58, -116.30, -6.13)],
}

WORDMARKS = {
    'saira': dict(fit='width'),
    'sairaLock': dict(fit='tracking', tracking=110),
}


def wedge(side, x, yt, yb):
    """A triangle that masks off one stroke end along the cut line."""
    h = yb - yt
    off = SLOPE * h
    e = 0.12
    if side == 'R':
        point = lambda t: (x - off * t, yt + h * t)
        far = x + 30
    else:
        point = lambda t: (x + off - off * t, yt + h * t)
        far = x - 30
    pts = [point(-e), (far, yt - e * h), (far, yb + e * h), point(1 + e)]
    return 'M' + 'L'.join(f'{a:.1f} {b:.1f}' for a, b in pts) + 'Z'


def main():
    font = instantiateVariableFont(TTFont('fonts/Saira.ttf'), {'wdth': 125, 'wght': 600})
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    glyphs = [(ch, gs[cmap[ord(ch)]]) for ch in 'TECH']

    def bounds(g):
        pen = BoundsPen(gs)
        g.draw(pen)
        return pen.bounds

    advances = [g.width for _, g in glyphs]
    first_left = bounds(glyphs[0][1])[0]
    last_right = bounds(glyphs[-1][1])[2]

    out = []
    for name, spec in WORDMARKS.items():
        if spec['fit'] == 'width':
            scale = 27.5 / 688  # cap height 27.5 units in the stacked layout
            ink = sum(advances[:-1]) + last_right - first_left
            tracking = ((MARK_R - MARK_L) / scale - ink) / (len(glyphs) - 1)
        else:
            tracking = spec['tracking']
        paths, wedges, x = [], [], 0
        for (ch, g), w in zip(glyphs, advances):
            pen = SVGPathPen(gs)
            g.draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
            paths.append(pen.getCommands())
            for side, cx, yt, yb in SAIRA_CUTS.get(ch, []):
                wedges.append(wedge(side, cx + x, yt, yb))
            x += w + tracking
        right = x - tracking - advances[-1] + last_right
        out.append(
            f'<mask id="cut-{name}" maskUnits="userSpaceOnUse" x="-500" y="-1200" width="{right + 1000:.0f}" height="1700">'
            f'<rect x="-500" y="-1200" width="{right + 1000:.0f}" height="1700" fill="#fff"/>'
            f'<path d="{"".join(wedges)}" fill="#000"/></mask>'
            f'<g id="w-{name}" mask="url(#cut-{name})"><path d="{"".join(paths)}" fill="var(--ink)"/></g>'
        )
        print(f'{name}: tracking {tracking:.0f}')

    os.makedirs('build', exist_ok=True)
    with open('build/wordmarks.defs.svg', 'w') as f:
        f.write('\n'.join(out))


if __name__ == '__main__':
    main()
