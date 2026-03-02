# tweakcc-minimal

Minimal system prompts for Claude Code. 

**Principle**: System prompts provide tool access and safety rails. CLAUDE.md/AGENTS.md provide workflow and conventions. Inspired by [Pi's context engineering](https://lucumr.pocoo.org/2026/1/31/pi/).

23 files changed, -47k chars (~10% of total), targeting the verbose files that override CLAUDE.md. Some tools were converted to stubs and moved to skills

## Quick start

```sh
# 1. Clone into ~/.tweakcc
git clone https://github.com/wassname/tweakcc-minimal ~/.tweakcc

# 2. Backup, patch in place, save patched copy
VERSION=$(claude --version | head -1 | cut -d' ' -f1)
BINARY=~/.local/share/claude/versions/$VERSION
cp "$BINARY" ~/.tweakcc/native-binary.backup          # unpatched backup
npx tweakcc --apply                                    # patches $BINARY in place
cp "$BINARY" ~/.local/share/claude/versions/${VERSION}-min  # save as -min
cp ~/.tweakcc/native-binary.backup "$BINARY"          # restore stock binary

# 3. Create symlinks so both versions coexist
ln -sf ~/.local/share/claude/versions/${VERSION}-min ~/.local/bin/claude-mn  # patched
# claude symlink already points to $VERSION (stock, now restored)


# 4.Install skills (optional, some tools converted to stub+skills)
mkdir -p ~/.claude/skills
ln -s $PWD/skills/* ~/.claude/skills
```

Now `claude` = stock, `claude-mn` = minimal prompts.

## Re-apply after edits

Edit `.md` files in `system-prompts/`, then:

```sh
VERSION=$(claude --version | head -1 | cut -d' ' -f1)
cp ~/.tweakcc/native-binary.backup ~/.local/share/claude/versions/${VERSION}-min
npx tweakcc --apply
```

## Disable auto-updates

CC auto-updates overwrite patched binaries:

```jsonc
// ~/.claude/settings.json
{ "autoUpdates": false }
```

Or via `env` in `~/.claude/settings.json`:

```jsonc
{ "env": { "DISABLE_AUTOUPDATER": "1" } }
```


## Key files to edit

| File | Controls |
|------|----------|
| `system-reminder-plan-mode-is-active-5-phase.md` | Plan mode workflow (was overriding CLAUDE.md) |
| `system-reminder-plan-mode-is-active-iterative.md` | Iterative plan mode variant |
| `system-prompt-main-system-prompt.md` | Role definition, ~10 lines |
| `system-prompt-doing-tasks.md` | Task execution rules + tool hints |
| `system-prompt-tone-and-style.md` | Output style |
| `system-prompt-tool-usage-policy.md` | Parallel calls, tool preferences |
| `system-prompt-hooks-configuration.md` | Hook event definitions (don't drop events) |

~200 files untouched (already 6-8 lines, tool descriptions, agent/skill prompts loaded on-demand).

## What changed



| File | Before | After | Notes |
|------|--------|-------|-------|
| plan-mode-5-phase | 90 | 20 | Defers to CLAUDE.md for workflow |
| plan-mode-iterative | 61 | 18 | Same |
| main-system-prompt | 17 | 10 | Pi-style minimal |
| doing-tasks | 18 | 7 | "Read first, follow CLAUDE.md" |
| learning-mode | 80 | 11 | Kept core, cut examples |
| insights-* (5 files) | 170 | 45 | Kept JSON schema, cut examples |
| hooks-configuration | 163 | 33 | Kept structure + all events, cut examples |
| mcp-cli | 124 | 25 | Kept commands, cut 6x repeated examples |

## Links

- [tweakcc](https://github.com/Piebald-AI/tweakcc) | [CC system prompts source](https://github.com/Piebald-AI/claude-code-system-prompts)
- [Pi system prompt](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/src/core/system-prompt.ts) | [Armin's blog](https://lucumr.pocoo.org/2026/1/31/pi/)
- Other mods: [bl-ue/tweakcc-system-prompts](https://github.com/bl-ue/tweakcc-system-prompts) | [yansircc/tweakcc-prompts](https://github.com/yansircc/tweakcc-prompts) | [principled-claude-code](https://github.com/m0n0x41d/principled-claude-code)
- [Trail of Bits Claude Code Config](https://github.com/trailofbits/claude-code-config)
- [Internals](https://www.southbridge.ai/blog/claude-code-an-analysis)
