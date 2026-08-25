set shell := ["bash", "-cu"]

default:
    @just --list

# Phase 1: Install fresh CC and back up clean binary
install version:
    #!/bin/bash -eu
    bun install @anthropic-ai/claude-code@{{ version }}
    # bun blocks postinstall; run manually to get the native binary
    node node_modules/@anthropic-ai/claude-code/install.cjs
    BINARY="node_modules/@anthropic-ai/claude-code/bin/claude.exe"
    BACKUP="DO_NOT_DELETE_patched_binaries/{{ version }}/native/original"
    mkdir -p "$(dirname "$BACKUP")"
    if [[ ! -f "$BACKUP" ]]; then
        cp "$BINARY" "$BACKUP"
        echo "backed up clean binary -> $BACKUP"
    else
        echo "backup already exists at $BACKUP"
    fi
    # update config.json version so extract/apply use correct backup path
    jq '.ccVersion = "{{ version }}"' config.json > config.json.tmp && mv config.json.tmp config.json
    echo "installed CC {{ version }}"

# Phase 2: Extract stock prompts from clean binary into stock-reference/
extract:
    #!/bin/bash -eu
    BINARY="node_modules/@anthropic-ai/claude-code/bin/claude.exe"
    VERSION=$(jq -r .ccVersion config.json)
    BACKUP="DO_NOT_DELETE_patched_binaries/$VERSION/native/original"
    # restore clean binary, remove tweakcc's internal backup
    # rm-first (unlink) avoids ETXTBSY when run from this same binary -- Claude
    rm -f "$BINARY"; cp "$BACKUP" "$BINARY"
    rm -f native-binary.backup native-binary.pre-reinstall.backup
    # clear system-prompts so tweakcc generates pure stock
    rm -f system-prompts/*.md 2>/dev/null || true
    # apply (generates stock .md files + prompt cache); -y: 4.3.x needs non-interactive confirm -- Claude
    bunx tweakcc --apply -y
    # save stock reference (may be empty if prompts not available for this version)
    rm -rf stock-reference
    mkdir -p stock-reference
    if ls system-prompts/*.md >/dev/null 2>&1; then
        cp system-prompts/*.md stock-reference/
    fi
    # restore clean binary (undo patching)
    rm -f "$BINARY"; cp "$BACKUP" "$BINARY"
    rm -f native-binary.backup
    # clear system-prompts again
    rm -f system-prompts/*.md 2>/dev/null || true
    COUNT=$(ls stock-reference/*.md 2>/dev/null | wc -l)
    echo "extracted $COUNT stock prompts to stock-reference/"
    if [[ "$COUNT" -eq 0 ]]; then
        echo "WARN: no prompts extracted (tweakcc may not support this CC version yet)"
    fi

# Phase 5: Apply customizations from system-prompts/ to clean binary
apply:
    #!/bin/bash -eu
    BINARY="node_modules/@anthropic-ai/claude-code/bin/claude.exe"
    VERSION=$(jq -r .ccVersion config.json)
    BACKUP="DO_NOT_DELETE_patched_binaries/$VERSION/native/original"
    # always start from clean
    # rm-first (unlink) avoids ETXTBSY when run from this same binary -- Claude
    rm -f "$BINARY"; cp "$BACKUP" "$BINARY"
    # remove tweakcc's internal backup so it doesn't restore a stale patched copy
    rm -f native-binary.backup native-binary.pre-reinstall.backup
    echo "restored clean binary from $BACKUP"
    # single apply (capture output: tweakcc reports which prompts it could not patch)
    mkdir -p out
    bunx tweakcc --apply -y 2>&1 | tee out/apply.log
    # remove stock files (keep only CUSTOM_FILES)
    python3 scripts/cleanup_stock_prompts.py
    # validate: template vars declared, AND every customization actually landed
    python3 scripts/audit_templates.py
    python3 scripts/check_landed.py out/apply.log
    # VERY IMPORTANT -- DO NOT SKIP. check_landed only believes tweakcc's own report;
    # this greps the binary bytes for every custom body. The user wants this proof. -- Claude
    python3 scripts/verify_in_binary.py | tee out/verify.log

# Phase 6: Smoke test
smoke:
    #!/bin/bash -eu
    BINARY="node_modules/@anthropic-ai/claude-code/bin/claude.exe"
    export CLAUDECODE=
    # anti-stacking check: the "(tweakcc)" version line must never appear >1x (=stacked patches).
    # 0 is fine: tweakcc 4.0.13 can't write the cosmetic version-indicator into newer CC binaries.
    # The canary below is the real proof the system-prompt patch landed; the version line is not.
    VERSION_OUT=$("$BINARY" -v 2>&1)
    echo "$VERSION_OUT"
    TWEAKCC_COUNT=$(echo "$VERSION_OUT" | grep -c "tweakcc" || true)
    if [[ "$TWEAKCC_COUNT" -gt 1 ]]; then
        echo "FAIL: $TWEAKCC_COUNT tweakcc version lines (binary patched multiple times?)"
        exit 1
    fi
    # canary check: webfetch description must contain our custom "evidence" line (real UAT)
    "$BINARY" -p "what is the description of your web fetch tool please, just copy paste it" --model haiku | grep evidence

# Phase 7: Back up patched binary, publish binaries to GitHub releases
ship version:
    #!/bin/bash -eu
    BINARY="node_modules/@anthropic-ai/claude-code/bin/claude.exe"
    PATCHED="DO_NOT_DELETE_patched_binaries/{{ version }}/native/patched"
    mkdir -p "$(dirname "$PATCHED")"
    if [[ ! -f "$PATCHED" ]]; then
        cp "$BINARY" "$PATCHED"
        echo "archived patched binary -> $PATCHED"
    fi
    ln -sf "$(realpath "$BINARY")" "$HOME/.local/bin/claude"
    echo "claude symlink -> $(realpath "$BINARY")"
    just release {{ version }}

# Upload original + patched binaries as GitHub release assets (private repo)
release version:
    #!/bin/bash -eu
    ORIGINAL="DO_NOT_DELETE_patched_binaries/{{ version }}/native/original"
    PATCHED="DO_NOT_DELETE_patched_binaries/{{ version }}/native/patched"
    TAG="v{{ version }}"
    gh release create "$TAG" "$ORIGINAL" "$PATCHED" \
        --title "Claude Code {{ version }}" \
        --notes "clean original + tweakcc-patched native binaries" \
        || gh release upload "$TAG" "$ORIGINAL" "$PATCHED" --clobber
    echo "released $TAG -> $ORIGINAL $PATCHED"

# Download a version's binaries from GitHub releases (fresh box)
fetch-binary version:
    #!/bin/bash -eu
    DEST="DO_NOT_DELETE_patched_binaries/{{ version }}/native"
    mkdir -p "$DEST"
    gh release download "v{{ version }}" --dir "$DEST" --clobber
    ls -la "$DEST"
