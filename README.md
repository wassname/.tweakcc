# tweakcc-minimal

Minimal system prompts for Claude Code, inspired by [Pi's approach](https://lucumr.pocoo.org/2026/1/31/pi/) to context engineering.

## Sources

- Pi system prompt: https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/src/core/system-prompt.ts
- Pi compaction: https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/src/core/compaction/compaction.ts
- Armin's blog on Pi: https://lucumr.pocoo.org/2026/1/31/pi/
- tweakcc: https://github.com/Piebald-AI/tweakcc
- CC system prompts source: https://github.com/Piebald-AI/claude-code-system-prompts

## Problem

Claude Code's default system prompts are ~11k lines across 222 files. They prescribe rigid workflows (5-phase planning, verbose doing-tasks rules) that override user instructions in CLAUDE.md/AGENTS.md. The model doesn't listen to your project conventions.

## Principle

Make system prompts minimal and explicitly defer to CLAUDE.md / AGENTS.md as primary instructions. Pi's coding agent has ~40 lines of system prompt. Ours doesn't need to be that extreme, but the system prompt should set up tools and safety, not dictate workflow.

Key rules:
- System prompts provide tool access and safety rails
- CLAUDE.md / AGENTS.md provide workflow, conventions, style
- Plan mode says "follow CLAUDE.md" not "do these 5 phases"
- No verbose examples or hand-holding in the system prompt

## What changed

23 files edited, +98 -838 lines. See `git diff` for details.

| File | Before | After | Notes |
|------|--------|-------|-------|
| plan-mode-5-phase | 90 lines | 20 lines | Defers to CLAUDE.md for workflow |
| plan-mode-iterative | 61 lines | 18 lines | Same |
| plan-mode-subagent | 16 lines | 12 lines | Same |
| plan-mode-re-entry | 23 lines | 10 lines | Same |
| main-system-prompt | 17 lines | 10 lines | Pi-style minimal |
| doing-tasks | 18 lines | 7 lines | "Read first, don't over-engineer, follow CLAUDE.md" |
| tool-usage-policy | 18 lines | 8 lines | Keep parallel + prefer specialized tools |
| tone-and-style | 19 lines | 7 lines | Defer to CLAUDE.md |
| executing-actions-with-care | 15 lines | 6 lines | "Confirm before destructive" |
| learning-mode | 80 lines | 11 lines | Kept core, cut examples |
| learning-mode-insights | 15 lines | 7 lines | Kept core |
| insights-* (5 files) | 170 lines | 45 lines | Kept JSON schema, cut examples |
| skillify-current-session | 139 lines | 22 lines | Kept steps, cut examples |
| hooks-configuration | 163 lines | 33 lines | Kept structure ref, cut examples |
| mcp-cli | 124 lines | 25 lines | Kept commands, cut 6x repeated examples |
| task-management | 53 lines | 8 lines | 1 line rule, cut examples |
| chrome-browser-automation | 51 lines | 11 lines | Kept rules, cut verbose explanations |
| conditional-delegate | 23 lines | 9 lines | 1 line rule |
| scratchpad-directory | 22 lines | 7 lines | 1 line rule |

Untouched (already minimal or loaded on-demand):
- doing-tasks-* (13 sub-files, 6-8 lines each)
- tool-usage-* (11 sub-files, 8 lines each)
- tool-description-*, agent-prompt-*, data-*, skill-*
- system-reminder-* (38 notification files, 6-19 lines each)

## Current setup

```
~/.local/share/claude/versions/
  2.1.44       # original (unpatched)
  2.1.44-min   # patched with minimal prompts  <-- symlinked as `claude`
  2.1.63       # newer version (unpatched)

~/.local/bin/claude -> ~/.local/share/claude/versions/2.1.44-min
```

- Claude Code version: **2.1.44**
- tweakcc version: **4.0.10**
- Date: 2026-03-02
- Unpatched backup: `~/.tweakcc/native-binary.backup` (sha256 prefix: 090ed3f0)

To switch between original and minimal:
```sh
# Use minimal (current)
ln -sf ~/.local/share/claude/versions/2.1.44-min ~/.local/bin/claude

# Use original
ln -sf ~/.local/share/claude/versions/2.1.44 ~/.local/bin/claude
```

## How to use

### Apply patches to current CC install

```sh
npx tweakcc --apply
```

### Restore to original

```sh
npx tweakcc --restore
```

### Make a backup of a specific version before patching

```sh
# CC stores versions at ~/.local/share/claude/versions/
cp ~/.local/share/claude/versions/2.1.44 ~/.local/share/claude/versions/2.1.44.bak

# Or tweakcc already keeps one at:
# ~/.tweakcc/native-binary.backup
```

### Run a specific version

```sh
# Check which versions exist
ls ~/.local/share/claude/versions/

# Symlink points to active version
ls -la ~/.local/bin/claude
# -> ~/.local/share/claude/versions/2.1.44

# To switch versions (careful: CC auto-updates may overwrite)
ln -sf ~/.local/share/claude/versions/2.1.63 ~/.local/bin/claude

# Or run directly without switching
~/.local/share/claude/versions/2.1.63
```

### Create a standalone minimal binary

```sh
# 1. Copy the version you want to patch
cp ~/.local/share/claude/versions/2.1.44 ~/.local/share/claude/versions/2.1.44-min

# 2. Point tweakcc at it (tweakcc patches whatever ~/.local/bin/claude points to)
ln -sf ~/.local/share/claude/versions/2.1.44-min ~/.local/bin/claude

# 3. Apply
npx tweakcc --apply

# 4. Point back to your main version
ln -sf ~/.local/share/claude/versions/2.1.44 ~/.local/bin/claude

# 5. Run the minimal version directly
~/.local/share/claude/versions/2.1.44-min
```

### Extract/repack JS (for deeper edits)

```sh
# Extract JS from native binary
npx tweakcc unpack /tmp/claude-cli.js ~/.local/share/claude/versions/2.1.44

# Edit the JS directly if needed, then repack
npx tweakcc repack /tmp/claude-cli.js ~/.local/share/claude/versions/2.1.44-custom
```

### After CC auto-updates

CC may auto-update and overwrite the patched binary. Re-apply:

```sh
npx tweakcc --apply
```

The .md files in `system-prompts/` are your source of truth. The binary is just the compiled output.

## Remaining unchanged files

Already minimal (1-2 lines of content each), functional plumbing, or loaded on-demand:

- doing-tasks-* (13 sub-files, 6-8 lines each)
- tool-usage-* (11 sub-files, 8 lines each)
- agent-memory-instructions, agent-summary-generation, censoring-assistance
- chrome-browser-mcp-tools, context-compaction-summary
- git-status, option-previewer, parallel-tool-call-note
- teammate-communication, worker-instructions
- tone-code-references, tone-concise-output-*
- tool-execution-denied, tool-permission-mode
- system-reminder-* (38 notification files, 6-33 lines each)

## Ecosystem

### Alternative agents (require API key)

- [Pi](https://github.com/badlogic/pi-mono) - ~40 line system prompt, inspiration for this repo
- [OpenCode](https://github.com/anomalyco/opencode) - CC alternative with skill system

### Tools

- [ccusage](https://github.com/ryoppippi/ccusage) - usage tracking
- [ccstatusline](https://github.com/sirmalloc/ccstatusline) - fast Rust statusline

### Other system prompt mods

| Repo | Notes |
|------|-------|
| [Piebald-AI/tweakcc](https://github.com/Piebald-AI/tweakcc) | the patcher this repo uses |
| [bl-ue/tweakcc-system-prompts](https://github.com/bl-ue/tweakcc-system-prompts) | ~48k bytes smaller, 30% faster, same accuracy |
| [yansircc/tweakcc-prompts](https://github.com/yansircc/tweakcc-prompts) | Chinese-optimized + performance patches |
| [m0n0x41d/principled-claude-code](https://github.com/m0n0x41d/principled-claude-code) | FPF framework prompts, tier-scaled constraints |
| [ykdojo/claude-code-tips](https://github.com/ykdojo/claude-code-tips) | tips including "cutting the system prompt in half" |

### Config

- [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config) - good defaults from a security firm

### Appending prompts without patching

Simpler alternative - append a system prompt at invocation:

```sh
claude --append-system-prompt "$(cat ROLE.md)" --permission-mode acceptEdits \
  "Read @SPEC.md and start implementing"
```

See [issue #6153](https://github.com/anthropics/claude-code/issues/6153).

### Headless usage (`claude -p`)

| Goal | Command |
|------|---------|
| Simple chat | `echo "hi" \| claude -p` |
| JSON response | `claude -p --output-format json` |
| No tools | `claude -p --tools ""` |
| Full autonomy | `claude -p --permission-mode bypassPermissions` |
| Custom persona | `claude -p --system-prompt "..."` |
| Fast/cheap | `claude -p --model haiku` |
| Best quality | `claude -p --model opus` |

### Bug-fix patchers

- [LSP fix 2.1.2](https://gist.github.com/paulditerwich/77448b526e4940f27f6de41421014c02)
- [fix freeze on /dev/*](https://gist.github.com/heeen/b6ced51aeac9da1b315776f38752c4ff)

## Future ideas

- Minimize the doing-tasks-* sub-files (or confirm they're dead code in 2.1.44+)
- Make plan mode more brainstorm/research oriented with user
- Pin CC version to prevent auto-update overwriting patches
- Measure actual token savings in prompt cache
