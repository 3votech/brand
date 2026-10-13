"""Build guidelines/brand-guidelines.html from guidelines/template.html, inlining the logos as data URIs.

Usage: python3 scripts/guidelines.py logos guidelines/template.html guidelines/brand-guidelines.html
"""
import base64, os, re, sys
src, tpl, out = sys.argv[1:4]
s = open(tpl).read()
icons = {
 'yes': '<svg viewBox="0 0 20 20" aria-label="Do" role="img"><circle cx="10" cy="10" r="9" fill="currentColor"/><path d="M5.8 10.3l2.8 2.8 5.6-6" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 'no': '<svg viewBox="0 0 20 20" aria-label="Don\'t" role="img"><circle cx="10" cy="10" r="9" fill="currentColor"/><path d="M6.6 6.6l6.8 6.8M13.4 6.6l-6.8 6.8" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/></svg>',
}
def sub(m):
    k = m.group(1)
    if k in icons: return icons[k]
    data = open(os.path.join(src, f'3votech-{k}.svg'), 'rb').read()
    return 'data:image/svg+xml;base64,' + base64.b64encode(data).decode()
s = re.sub(r'\{\{([a-z-]+)\}\}', sub, s)
assert '{{' not in s
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w').write(s); print(len(s))
