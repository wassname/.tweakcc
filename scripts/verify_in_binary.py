#!/usr/bin/env python3
"""Prove each customization is really in the patched binary bytes.

check_landed.py only trusts tweakcc's own "could not find" report. This is the
independent check: grep the binary for a distinctive phrase from every custom
body. Prints the mandatory per-prompt report; exits 1 if any custom text is absent.

Columns:
  ours   = occurrences of a distinctive phrase from OUR body (must be >= 1)
  stock  = occurrences of a stock-only phrase we deliberately cut (informational:
           the binary holds several copies of some strings, so >0 is not a failure;
           the live check in `just smoke` is what proves which copy is served)
"""

import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent
binary = (root / 'node_modules/@anthropic-ai/claude-code/bin/claude.exe').read_bytes()


def body(path):
    text = path.read_text()
    return text.split('-->', 1)[1] if '-->' in text else text


def probes(text, n=8):
    """Distinctive greppable fragments. Backticks are escaped as \\` in our .md
    but plain in the binary, so split on them and keep the plain-prose runs."""
    out = []
    for line in text.splitlines():
        line = re.sub(r'\$\{[^}]*\}', '\x00', line)  # template vars: never match
        for seg in re.split(r'[`\x00]', line):
            seg = re.sub(r'\s+', ' ', seg.strip().lstrip('-*# ')).strip()
            seg = seg.replace('\\', '')
            if len(seg) >= 25:
                out.append(seg[:70])
    out.sort(key=len, reverse=True)
    return out[:n]


custom_dir = root / 'system-prompts'
stock_dir = root / 'stock-reference'
fails = []
rows = []

for f in sorted(custom_dir.glob('*.md')):
    ours = body(f)
    stock_path = stock_dir / f.name
    stock = body(stock_path) if stock_path.exists() else ''

    our_probes = probes(ours)
    our_hits = max((binary.count(p.encode()) for p in our_probes), default=0)

    ours_norm = re.sub(r'\s+', ' ', ours)
    stock_only = [p for p in probes(stock, 12) if p not in ours_norm]
    stock_hits = max((binary.count(p.encode()) for p in stock_only), default=0)

    rows.append((f.stem, len(our_probes), our_hits, stock_hits))
    if not our_probes:
        fails.append(f'{f.stem}: no usable probe (body too short/templated) -- verify by hand')
    elif our_hits == 0:
        fails.append(f'{f.stem}: OUR TEXT ABSENT from binary (patch did not land)')

print(f'{"prompt":<52} {"probes":>6} {"ours":>5} {"stock":>6}')
for stem, np, oh, sh in rows:
    print(f'{stem:<52} {np:>6} {oh:>5} {sh:>6}')

print()
if fails:
    print(f'FAIL ({len(fails)}):')
    for x in fails:
        print(' ', x)
    sys.exit(1)
print(f'OK: all {len(rows)}/{len(rows)} customizations found in binary bytes')
