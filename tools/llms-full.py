#!/usr/bin/env python3
"""Regenerate llms-full.txt from the built pages.

    python3 tools/llms-full.py

Reads index.html and vitalityos/index.html, strips scripts, styles and inline
image data, and writes the readable text with headings as markdown so answer
engines get the whole site in one fetch. Run after any copy change.
"""
import re, html, pathlib, datetime

REPO = pathlib.Path(__file__).resolve().parent.parent
PAGES = [
    ('https://cortexhealthai.com/', REPO / 'index.html'),
    ('https://cortexhealthai.com/vitalityos/', REPO / 'vitalityos' / 'index.html'),
]

def to_text(h):
    h = re.sub(r'<(script|style|noscript|svg)[\s\S]*?</\1>', ' ', h, flags=re.I)
    h = re.sub(r'data:[a-z]+/[a-z+.-]+;base64,[A-Za-z0-9+/=]+', '', h)
    h = re.sub(r'<!--[\s\S]*?-->', ' ', h)
    h = re.sub(r'<h1[^>]*>', '\n\n# ', h, flags=re.I)
    h = re.sub(r'<h2[^>]*>', '\n\n## ', h, flags=re.I)
    h = re.sub(r'<h3[^>]*>', '\n\n### ', h, flags=re.I)
    h = re.sub(r'<h4[^>]*>', '\n\n#### ', h, flags=re.I)
    h = re.sub(r'<li(?=[\s>])[^>]*>', '\n- ', h, flags=re.I)   # <li> only, not <link>
    h = re.sub(r'</(p|div|section|article|li|h[1-6]|tr|figcaption|blockquote|footer|header)>', '\n', h, flags=re.I)
    h = re.sub(r'<br\s*/?>', '\n', h, flags=re.I)
    h = re.sub(r'<(td|th)[^>]*>', ' | ', h, flags=re.I)
    h = re.sub(r'<[^>]+>', ' ', h)
    t = html.unescape(h)
    t = re.sub(r'[ \t ]+', ' ', t)
    t = re.sub(r' *\n *', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()

out = ['# CORTEX Health AI, full site text',
       f'Generated {datetime.date.today().isoformat()} from the published pages. The fact file is https://cortexhealthai.com/llms.txt.',
       '']
for url, path in PAGES:
    out.append(f'\n\n---\n\nSOURCE: {url}\n')
    out.append(to_text(path.read_text(encoding='utf-8')))
(REPO / 'llms-full.txt').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('wrote llms-full.txt', (REPO / 'llms-full.txt').stat().st_size, 'bytes')
