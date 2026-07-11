#!/usr/bin/env python3
"""Fail if any of OUR customizations did not land in the patched binary.

tweakcc locates each stock prompt by a whole-prompt regex built from its prompt
data, then replaces it with our body. If upstream text drifted even slightly,
that regex misses and our customization is SILENTLY skipped -- the binary keeps
the stock prompt. tweakcc prints `Could not find system prompt "<name>"` for
each miss. We fail the build if any of our custom prompt names show up there.

This is the gate that catches silent divergence: a canary on one prompt (the
smoke test) does not prove the other 19 landed.

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
    m = re.search(r"^name:\s*(.+?)\s*$", f.read_text(encoding='utf-8'), re.M)
    if m:
        names.add(m.group(1).strip().strip('\'"'))

text = log.read_text(encoding='utf-8', errors='ignore')
notfound = set(re.findall(r'Could not find system prompt "([^"]+)"', text))
failed = sorted(names & notfound)

if failed:
    print(f'FAIL: {len(failed)}/{len(names)} customization(s) did NOT land '
          f'(tweakcc regex missed the stock text; binary keeps stock):')
    for n in failed:
        print(f'  - {n}')
    sys.exit(1)

print(f'OK: all {len(names)} customizations landed (none in tweakcc could-not-find list)')
