#!/usr/bin/env python3
"""Template integrity audit: every used ${VAR...} must be declared in header variables."""

import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent / 'system-prompts'
pat = re.compile(r'\$\{([^}]+)\}')
issues = []

for path in sorted(root.glob('*.md')):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('<!--') or '-->' not in text:
        continue
    head, body = text.split('-->', 1)

    declared = []
    in_vars = False
    for line in head.splitlines():
        if re.match(r'^\s*variables\s*:\s*$', line):
            in_vars = True
            continue
        if in_vars:
            m = re.match(r'^\s*-\s*([A-Z0-9_]+)\s*$', line)
            if m:
                declared.append(m.group(1))
                continue
            if line.strip() == '' or line.strip().startswith('#'):
                continue
            if not line.startswith('  '):
                in_vars = False

    declared_set = set(declared)
    used = set()
    for m in pat.finditer(body):
        expr = m.group(1).strip()
        sm = re.match(r'([A-Z][A-Z0-9_]*)(?:\s*\(|\b)', expr)
        if sm:
            used.add(sm.group(1))

    missing = sorted(x for x in used if x not in declared_set)
    if missing:
        issues.append((path.name, missing))

if issues:
    for name, missing in issues:
        print(f"{name}: undeclared -> {', '.join(missing)}")
    sys.exit(1)

print('OK: all used template vars are declared')
