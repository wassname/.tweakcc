set shell := ["bash", "-cu"]

default:
    @just --list

# Discover all Claude installations, patch each, audit templates.
apply:
    node scripts/patch_all.mjs
    python3 scripts/audit_templates.py

# Patch a specific Claude binary by path (e.g. snap native binary).
patch path:
    node scripts/patch_all.mjs {{ path }}

# Create ~/.local/bin symlinks: claude-native-{ver}, claude-native-tcc-{ver}, claude-npm-tcc-{ver}
link-versions:
    #!/bin/bash -eu
    BINDIR="$HOME/.local/bin"
    # stock native binaries from ~/.local/share/claude/versions/
    for bin in "$HOME/.local/share/claude/versions"/*; do
    	ver=$(basename "$bin")
    	slug="${ver//./-}"
    	ln -sf "$bin" "$BINDIR/claude-native-$slug"
    	echo "linked claude-native-$slug -> $bin"
    done
    # tweakcc-patched native binaries from out/*/native/patched
    for bin in "{{ justfile_directory() }}/out"/*/native/patched; do
    	ver=$(basename "$(dirname "$(dirname "$bin")")")
    	slug="${ver//./-}"
    	ln -sf "$bin" "$BINDIR/claude-native-tcc-$slug"
    	echo "linked claude-native-tcc-$slug -> $bin"
    done
    # tweakcc-patched npm versions from out/*/npm/patched.js (needs a node wrapper)
    latest_wrapper=""
    for js in "{{ justfile_directory() }}/out"/*/npm/patched.js; do
    	ver=$(basename "$(dirname "$(dirname "$js")")")
    	slug="${ver//./-}"
    	wrapper="$BINDIR/claude-npm-tcc-$slug"
    	printf '#!/bin/bash\nexec node "%s" "$@"\n' "$js" > "$wrapper"
    	chmod +x "$wrapper"
    	echo "linked claude-npm-tcc-$slug -> $js"
    	latest_wrapper="$wrapper"
    done
    # set claude -> latest patched npm version
    if [[ -n "$latest_wrapper" ]]; then
    	ln -sf "$latest_wrapper" "$BINDIR/claude"
    	echo "default: claude -> $latest_wrapper"
    fi

# Reinstall Claude Code from npm, then apply tweaks to all installations.
fresh version="2.1.63":
    rm -f cli.js.backup native-binary.backup native-binary.pre-reinstall.backup
    rm -rf out
    npm install -g "@anthropic-ai/claude-code@{{ version }}"
    just apply

smoke:
    #!/bin/bash -eu
    # should contain tweakcc
    claude -d -v
    # should contain word evidence we put in the description of the web fetch tool in the template
    claude -p "what is the description of your web fetch tool please, from context" --model haiku --permission-mode=dontAsk -d | grep evidence
