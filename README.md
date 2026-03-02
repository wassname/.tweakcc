# tweakcc-minimal

Minimal system prompts for Claude Code via [tweakcc](https://github.com/Piebald-AI/tweakcc), inspired by [Pi's context engineering](https://lucumr.pocoo.org/2026/1/31/pi/).

**Problem**: CC's ~11k lines of system prompts prescribe rigid workflows (5-phase planning, verbose task rules) that override CLAUDE.md/AGENTS.md. The model doesn't listen to your project conventions.

**Principle**: System prompts provide tool access and safety rails. CLAUDE.md/AGENTS.md provide workflow, conventions, style. Plan mode says "follow CLAUDE.md" not "do these 5 phases".

## What changed

23 files, +98 -838 lines, ~47k chars removed. `git log --oneline` for details.

| File | Before | After | Notes |
|------|--------|-------|-------|
| plan-mode-5-phase | 90 | 20 | Defers to CLAUDE.md for workflow |
| plan-mode-iterative | 61 | 18 | Same |
| plan-mode-subagent | 16 | 12 | Same |
| plan-mode-re-entry | 23 | 10 | Same |
| main-system-prompt | 17 | 10 | Pi-style minimal |
| doing-tasks | 18 | 7 | "Read first, follow CLAUDE.md" |
| tool-usage-policy | 18 | 8 | Parallel calls, prefer specialized tools |
| tone-and-style | 19 | 7 | Defer to CLAUDE.md |
| executing-actions-with-care | 15 | 6 | "Confirm before destructive" |
| learning-mode | 80 | 11 | Kept core, cut examples |
| insights-* (5 files) | 170 | 45 | Kept JSON schema, cut examples |
| skillify-current-session | 139 | 22 | Kept steps, cut examples |
| hooks-configuration | 163 | 33 | Kept structure + all events, cut examples |
| mcp-cli | 124 | 25 | Kept commands, cut 6x repeated examples |
| task-management | 53 | 8 | 1 line rule |
| chrome-browser-automation | 51 | 11 | Kept rules only |
| conditional-delegate | 23 | 9 | 1 line rule |
| scratchpad-directory | 22 | 7 | 1 line rule |

~200 files untouched (already 6-8 lines, tool descriptions, agent/skill prompts loaded on-demand).

## Key files to edit

For future tweaks, these are the high-impact files:

| File | Controls |
|------|----------|
| `system-reminder-plan-mode-is-active-5-phase.md` | Plan mode workflow (was overriding CLAUDE.md) |
| `system-reminder-plan-mode-is-active-iterative.md` | Iterative plan mode variant |
| `system-prompt-main-system-prompt.md` | Role definition, ~10 lines |
| `system-prompt-doing-tasks.md` | Task execution rules + tool hints |
| `system-prompt-tone-and-style.md` | Output style |
| `system-prompt-tool-usage-policy.md` | Parallel calls, tool preferences |
| `system-prompt-executing-actions-with-care.md` | Destructive action guardrails |
| `system-prompt-hooks-configuration.md` | Hook event definitions (don't drop events) |

After editing, re-apply:
```sh
cp ~/.tweakcc/native-binary.backup ~/.local/share/claude/versions/2.1.44-min
ln -sf ~/.local/share/claude/versions/2.1.44-min ~/.local/bin/claude
npx tweakcc --apply
```

## Setup

CC version: **2.1.44** | tweakcc: **4.0.10** | Date: 2026-03-02

```
~/.local/share/claude/versions/
  2.1.44       # original (unpatched)
  2.1.44-min   # patched with minimal prompts  <-- symlinked as `claude`
  2.1.63       # newer version (unpatched)

~/.local/bin/claude -> ~/.local/share/claude/versions/2.1.44-min
```

Unpatched backup: `~/.tweakcc/native-binary.backup` (sha256 prefix: 090ed3f0)

Switch versions:
```sh
ln -sf ~/.local/share/claude/versions/2.1.44-min ~/.local/bin/claude  # minimal
ln -sf ~/.local/share/claude/versions/2.1.44 ~/.local/bin/claude      # original
```

### Disable auto-updates

CC auto-updates will overwrite patched binaries. Disable with:
```jsonc
// ~/.claude/settings.json
{ "autoUpdates": false }
```
Or env var `DISABLE_AUTOUPDATER=1`. See [issue #12564](https://github.com/anthropics/claude-code/issues/12564) for the naming inconsistency.

If auto-update does fire, just re-run `npx tweakcc --apply`. The .md files in `system-prompts/` are your source of truth.

## How to use

```sh
npx tweakcc --apply      # apply patches to whatever ~/.local/bin/claude points to
npx tweakcc --restore    # restore original
```

Create a standalone patched binary:
```sh
cp ~/.local/share/claude/versions/2.1.44 ~/.local/share/claude/versions/2.1.44-min
ln -sf ~/.local/share/claude/versions/2.1.44-min ~/.local/bin/claude
npx tweakcc --apply
ln -sf ~/.local/share/claude/versions/2.1.44 ~/.local/bin/claude  # switch back
~/.local/share/claude/versions/2.1.44-min  # run directly
```

Extract/repack JS for deeper edits:
```sh
npx tweakcc unpack /tmp/claude-cli.js ~/.local/share/claude/versions/2.1.44
npx tweakcc repack /tmp/claude-cli.js ~/.local/share/claude/versions/2.1.44-custom
```

---

## Appendix

### Sources

- [Pi system prompt](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/src/core/system-prompt.ts) | [Pi compaction](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/src/core/compaction/compaction.ts)
- [Armin's blog on Pi](https://lucumr.pocoo.org/2026/1/31/pi/)
- [tweakcc](https://github.com/Piebald-AI/tweakcc) | [CC system prompts source](https://github.com/Piebald-AI/claude-code-system-prompts)

### Ecosystem

Alternative agents: [Pi](https://github.com/badlogic/pi-mono) (~40 line system prompt) | [OpenCode](https://github.com/anomalyco/opencode) (skill system)

Tools: [ccusage](https://github.com/ryoppippi/ccusage) | [ccstatusline](https://github.com/sirmalloc/ccstatusline)

Config: [trailofbits/claude-code-config](https://github.com/trailofbits/claude-code-config)

| Other system prompt mods | Notes |
|------|-------|
| [bl-ue/tweakcc-system-prompts](https://github.com/bl-ue/tweakcc-system-prompts) | ~48k bytes smaller, 30% faster, same accuracy |
| [yansircc/tweakcc-prompts](https://github.com/yansircc/tweakcc-prompts) | Chinese-optimized + performance patches |
| [principled-claude-code](https://github.com/m0n0x41d/principled-claude-code) | FPF framework, tier-scaled constraints |
| [claude-code-tips](https://github.com/ykdojo/claude-code-tips) | tips including "cutting the system prompt in half" |

Bug-fix patchers: [LSP fix 2.1.2](https://gist.github.com/paulditerwich/77448b526e4940f27f6de41421014c02) | [fix freeze on /dev/*](https://gist.github.com/heeen/b6ced51aeac9da1b315776f38752c4ff)

### Appending prompts without patching

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
