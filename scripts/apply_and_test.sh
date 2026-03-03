#!/usr/bin/env bash
set -euo pipefail

# Purpose: patch the npm Claude CLI, then fail-fast on template/runtime regressions.

HOME_DIR="${HOME}"
NPM_CLAUDE="${HOME_DIR}/.nvm/versions/node/v22.22.0/bin/claude"
NPM_CLI_JS="${HOME_DIR}/.nvm/versions/node/v22.22.0/lib/node_modules/@anthropic-ai/claude-code/cli.js"
CONFIG="${HOME_DIR}/.tweakcc/config.json"

# 1) Pin tweakcc target to npm cli.js (avoid snap/other installs).
node -e "
const fs = require('fs')
const file = process.argv[1]
const target = process.argv[2]
const data = JSON.parse(fs.readFileSync(file, 'utf8'))
data.ccInstallationPath = target
fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n')
console.log('Updated ccInstallationPath -> ' + target)
" "$CONFIG" "$NPM_CLI_JS"

# 2) Ensure shell 'claude' resolves to npm launcher.
ln -sfn "$NPM_CLAUDE" "${HOME_DIR}/.local/bin/claude"

# 3) Save local backups of original/patched cli.js under out/<version>/.
VERSION="$(node -p "require('${HOME_DIR}/.nvm/versions/node/v22.22.0/lib/node_modules/@anthropic-ai/claude-code/package.json').version")"
OUT_DIR="out/${VERSION}"
mkdir -p "$OUT_DIR"
cp "$NPM_CLI_JS" "${OUT_DIR}/cli.js.orig"

# 4) Apply tweakcc customizations.
npx tweakcc --apply
cp "$NPM_CLI_JS" "${OUT_DIR}/cli.js.patched"

# 5) Template integrity audit: every used ${VAR...} must be declared in header variables.
python3 - <<'PY'
import pathlib
import re
import sys

root = pathlib.Path('system-prompts')
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
PY

# 6) Quick marker check: patched binary is active.
MARKER_OUT="$($NPM_CLAUDE -p ping -v 2>&1 || true)"
echo "$MARKER_OUT"
[[ "$MARKER_OUT" == *"Claude Code"* ]]
if [[ "$MARKER_OUT" != *"tweakcc"* ]]; then
    echo "WARN: tweakcc marker missing in -v output (often due known patchesAppliedIndication failure)." >&2
fi

# 7) Strict runtime test: stream-json ping must end in success (not error_during_execution).
python3 - <<'PY'
import json
import subprocess
import sys

cmd = [
    f"{__import__('os').environ['HOME']}/.nvm/versions/node/v22.22.0/bin/claude",
    '-p',
    'ping',
    '--output-format',
    'stream-json',
]
proc = subprocess.run(cmd, capture_output=True, text=True)
out = (proc.stdout or '') + (proc.stderr or '')
print(out, end='')

result = None
for line in out.splitlines():
    s = line.strip()
    if not s.startswith('{'):
        continue
    try:
        obj = json.loads(s)
    except Exception:
        continue
    if obj.get('type') == 'result':
        result = obj

if result is None:
    print('No result JSON found')
    sys.exit(1)
if result.get('subtype') != 'success':
    print(f"Runtime ping failed: subtype={result.get('subtype')}")
    sys.exit(1)
if result.get('errors'):
    print(f"Runtime errors: {result.get('errors')}")
    sys.exit(1)

print('OK: runtime ping succeeded')
PY
