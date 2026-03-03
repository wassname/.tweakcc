set shell := ["bash", "-cu"]

default:
	@just --list

# Apply tweaks to npm Claude, then run template and runtime checks.
apply:
	bash scripts/apply_and_test.sh

# Clean-reset install path, reinstall Claude Code, then apply+test.
fresh version="2.1.63":
	bash scripts/install_fresh.sh {{version}}
