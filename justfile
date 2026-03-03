set shell := ["bash", "-cu"]

default:
	@just --list

# Discover all Claude installations, patch each, audit templates.
apply:
	node scripts/patch_all.mjs
	python3 scripts/audit_templates.py

# Patch a specific Claude binary by path (e.g. snap native binary).
patch path:
	node scripts/patch_all.mjs {{path}}

# Reinstall Claude Code from npm, then apply tweaks to all installations.
fresh version="2.1.63":
	rm -f cli.js.backup native-binary.backup native-binary.pre-reinstall.backup
	rm -rf out
	npm install -g "@anthropic-ai/claude-code@{{version}}"
	just apply
