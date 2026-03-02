# tweakcc-minimal

Minimal system prompts for Claude Code. 

**Principle**: System prompts provide tool access and safety rails. CLAUDE.md/AGENTS.md provide workflow and conventions. Inspired by [Pi's context engineering](https://lucumr.pocoo.org/2026/1/31/pi/).

23 files changed, -47k chars (~10% of total), targeting the verbose files that override CLAUDE.md. Some tools were converted to stubs and moved to skills

Normally 24.6%     49.2k tokens
Now      16.5% · 33.1k tokens

## Quick start

```sh
# 1. Clone into ~/.tweakcc
git clone https://github.com/wassname/tweakcc-minimal ~/.tweakcc

# 2. Install Claude Code (npm/global target)
npm install -g @anthropic-ai/claude-code@2.1.63

# 3. Ensure tweakcc patches the npm/global cli.js
just set-node-target

# Optional but recommended: force shell `claude` to npm install
just fix-claude-link

# 4. Patch current install and save local backups in out/<version>/
just install

# 5. Test patched npm/global claude directly
just test

# 6. Optional: test what your shell resolves as `claude`
just test-shell

# 7.Install skills (optional, some tools converted to stub+skills)
mkdir -p ~/.claude/skills
ln -s $PWD/skills/* ~/.claude/skills
```

Backups are local to this repo at `out/<version>/cli.js.orig` and `out/<version>/cli.js.patched`.

## Troubleshooting

### `claude -p ping` returns `error_during_execution` (for example `EXPLORE_AGENT_VARIANT is not defined` or `GLOB_TOOL_NAME is not defined`)

This usually means one prompt template references a variable that is unavailable in your current runtime.

1. Search for the failing symbol:
	- `just diag-search-ping-error`
2. Fix the offending prompt template.
3. Re-apply patches:
	- `just apply`
4. Smoke test npm/global claude:
	- `just test`

If you are stuck in a restore/apply loop, use the recovery recipe below instead of repeating manual steps.

### Backup loop recovery (`tweakcc` backup is stale or already patched)

`tweakcc` keeps a backup of Claude Code (`cli.js` or native binary). Before applying customizations, it restores that backup to start from a clean base. If that backup is itself already modified, you can get stuck reapplying on top of old patched state.

Typical failure mode:

- You have a tweaked Claude binary.
- Backup is missing or stale.
- A new backup gets created from the already-modified binary.
- Reinstall + reapply still restores the stale modified backup.

Break the loop by forcing a fresh install and fresh backup:

- `just install-fresh`

This removes legacy tweakcc backups, clears local `out/`, reinstalls Claude Code, patches the npm/global `cli.js`, and writes fresh backups to `out/<version>/`.

Use this as a recovery path, not the normal workflow. Normal day-to-day flow should stay:

- `just install`

### `tweakcc` patches the wrong Claude install

If `npx tweakcc --apply` says it found Claude under a VS Code / snap path (for example `/home/.../snap/code-insiders/...`) but you want to patch npm's Node install, pin the target in `config.json`:

```json
{
	"ccInstallationPath": "/home/wassname/.nvm/versions/node/v22.22.0/lib/node_modules/@anthropic-ai/claude-code/cli.js"
}
```

Then re-run `just apply` and confirm output starts with:

- `Found Claude Code at: /home/.../.nvm/.../@anthropic-ai/claude-code/cli.js`

If your shell still resolves `claude` to a snap path like:

- `/home/.../snap/code-insiders/.../claude/versions/...`

run:

- `just fix-claude-link`

and verify with:

- `just paths`
- `just test-shell`

### One known failing patch on `2.1.63` (Node install)

On some `2.1.63` Node builds, `patches-applied-indication` fails with:

- `patch: patchesAppliedIndication: failed to find Claude Code version pattern`

Everything else can still patch correctly. If you want a fully clean run, apply an explicit allowlist that excludes that patch:

```sh
npx tweakcc --apply --patches "verbose-property,context-limit,model-customizations,opusplan1m,show-more-items-in-select-menus,fix-lsp-support,thinking-verbs,thinker-format,thinking-visibility,agents-md,session-memory,mcp-non-blocking,user-message-display"
```

This produces `Customizations applied successfully!` on the Node target above.

## Re-apply after edits

Edit `.md` files in `system-prompts/`, then:

```sh
just apply
just backup-patched
just test
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
