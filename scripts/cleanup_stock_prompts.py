#!/usr/bin/env python3
"""Remove stock prompt files from system-prompts/, keeping only explicit customizations.

After `tweakcc --apply`, system-prompts/ contains 313+ files: our customizations
plus stock copies regenerated from the binary. The stock copies must be deleted
because tweakcc's text representation uses ${VAR.property} expressions that become
literal JS template literals when patched back, causing ReferenceErrors at runtime
(e.g. WRITE_TOOL is not defined).

Only files listed in CUSTOM_FILES are kept. Everything else is deleted.
"""

import pathlib

root = pathlib.Path(__file__).resolve().parent.parent / 'system-prompts'

# Files we actively customize. Add new entries here when creating customizations.
CUSTOM_FILES = {
    'tool-description-webfetch',
}

deleted = 0
kept = 0
for f in sorted(root.glob('*.md')):
    if f.stem in CUSTOM_FILES:
        kept += 1
    else:
        f.unlink()
        deleted += 1

print(f'Deleted {deleted} stock files, kept {kept} customized')
