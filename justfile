set shell := ["bash", "-cu"]

NPM_CLAUDE := env_var("HOME") + "/.nvm/versions/node/v22.22.0/bin/claude"
NPM_CLI_JS := env_var("HOME") + "/.nvm/versions/node/v22.22.0/lib/node_modules/@anthropic-ai/claude-code/cli.js"
CONFIG := env_var("HOME") + "/.tweakcc/config.json"
VERSION := `node -p "require(process.env.HOME + '/.nvm/versions/node/v22.22.0/lib/node_modules/@anthropic-ai/claude-code/package.json').version"`
OUT_DIR := "out/" + VERSION
CLI_ORIG := OUT_DIR + "/cli.js.orig"
CLI_PATCHED := OUT_DIR + "/cli.js.patched"

default:
	@just --list

# Show where tweakcc patches and what shell `claude` resolves to.
paths:
	@echo "NPM_CLAUDE={{NPM_CLAUDE}}"
	@echo "NPM_CLI_JS={{NPM_CLI_JS}}"
	@echo "CONFIG={{CONFIG}}"
	@echo "VERSION={{VERSION}}"
	@echo "OUT_DIR={{OUT_DIR}}"
	@echo "shell_claude=$(command -v claude || true)"
	@echo "shell_claude_target=$(realpath "$(command -v claude || true)" 2>/dev/null || true)"

# Pin tweakcc to npm cli.js (avoid snap/other installs).
set-node-target:
	#!/usr/bin/env bash
	set -euo pipefail
	node -e "const fs=require('fs');const file='{{CONFIG}}';const data=JSON.parse(fs.readFileSync(file,'utf8'));data.ccInstallationPath='{{NPM_CLI_JS}}';fs.writeFileSync(file,JSON.stringify(data,null,2)+'\\n');console.log('Updated ccInstallationPath -> {{NPM_CLI_JS}}')"

# Ensure shell `claude` launches npm Claude, not a stale snap symlink.
fix-claude-link:
	ln -sfn "{{NPM_CLAUDE}}" "{{env_var("HOME")}}/.local/bin/claude"

# Create output dir for per-version local backups.
ensure-out:
	mkdir -p "{{OUT_DIR}}"

# Save clean original npm cli.js before applying tweaks.
backup-orig: ensure-out
	cp "{{NPM_CLI_JS}}" "{{CLI_ORIG}}"

# Apply tweakcc customizations to configured target.
apply:
	npx tweakcc --apply

# Save patched npm cli.js after applying tweaks.
backup-patched: ensure-out
	cp "{{NPM_CLI_JS}}" "{{CLI_PATCHED}}"

# Restore original npm cli.js from local backup.
restore-orig:
	cp "{{CLI_ORIG}}" "{{NPM_CLI_JS}}"

# Test npm Claude directly (bypasses shell path confusion).
test:
	#!/usr/bin/env bash
	set -euo pipefail
	out="$({{NPM_CLAUDE}} -p ping 2>&1 || true)"
	echo "$out"
	[[ "$out" != *"Execution error"* ]]
	[[ "$out" == *"pong"* ]]

# Test whatever your shell resolves for `claude`.
test-shell:
	#!/usr/bin/env bash
	set -euo pipefail
	out="$(claude -p ping 2>&1 || true)"
	echo "$out"
	[[ "$out" != *"Execution error"* ]]
	[[ "$out" == *"pong"* ]]

# Normal workflow: target npm cli.js, apply, backup patched, test.
install: set-node-target fix-claude-link backup-orig apply backup-patched test

# Recovery: clear legacy backups + local out/, reinstall, then normal install.
install-fresh version="2.1.63":
	rm -f ~/.tweakcc/cli.js.backup ~/.tweakcc/native-binary.backup ~/.tweakcc/native-binary.pre-reinstall.backup
	rm -rf out
	npm install -g @anthropic-ai/claude-code@{{version}}
	just install

# Find undefined-template crashes quickly.
diag-search-ping-error:
	rg -n "error_during_execution|is not defined|EXPLORE_AGENT_VARIANT|GLOB_TOOL_NAME" system-prompts README.md native-claudejs-*.js prompt-data-cache/*.json
