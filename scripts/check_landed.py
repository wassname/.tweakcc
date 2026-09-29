#!/usr/bin/env python3
"""Fail if tweakcc reports that one of OUR customizations did not match.

tweakcc locates each stock prompt by a whole-prompt regex built from its prompt
data, then replaces it with our body. If upstream text drifted even slightly,
that regex misses and our customization is SILENTLY skipped -- the binary keeps
the stock prompt. tweakcc prints `Could not find system prompt "<name>"` for
each miss. We fail the build if any of our custom prompt names show up there.

This catches prompt-regex divergence. verify_in_binary.py independently proves
that every custom body reached the binary.

Usage: check_landed.py <tweakcc-apply-log>
"""

import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent
sp = root / 'system-prompts'
log = pathlib.Path(sys.argv[1])

# our custom prompt display-names, from each file's frontmatter `name:`
names = set()
for f in sorted(sp.glob('*.md')):
    text = f.read_text(encoding='utf-8')
    m = re.search(r"^name:\s*(.*?)\s*$", text, re.M)
    if m:
        name = m.group(1)
        if name in {'>', '>-', '|', '|-'}:
            folded = []
            for line in text[m.end():].lstrip('\r\n').splitlines():
                if not line.startswith('  '):
                    break
                folded.append(line.strip())
            name = ' '.join(folded)
        names.add(name.strip().strip('\'"'))

text = log.read_text(encoding='utf-8', errors='ignore')
if 'Loading system prompts...' not in text or 'Applying customizations...' not in text:
    print('FAIL: input is not a complete tweakcc apply log')
    sys.exit(1)
notfound = set(re.findall(r'Could not find system prompt "([^"]+)"', text))
failed = sorted(names & notfound)

if failed:
    print(f'FAIL: {len(failed)}/{len(names)} customization(s) did NOT land '
          f'(tweakcc regex missed the stock text; binary keeps stock):')
    for n in failed:
        print(f'  - {n}')
    sys.exit(1)

print(f'OK: no custom prompt was reported missing ({len(names)} checked; byte verification follows)')
