# tweakcc-minimal

Minimal system prompts for Claude Code. 

**Principle**: System prompts provide tool access and safety rails. CLAUDE.md/AGENTS.md provide workflow and conventions. Inspired by [Pi's context engineering](https://lucumr.pocoo.org/2026/1/31/pi/).

23 files changed, -47k chars (~10% of total), targeting the verbose files or that override CLAUDE.md. Some tools were converted to stubs and moved to skills

Normally 24.6%     49.2k tokens
Now      16.5% · 33.0k tokens

### Micro-agent exception

`agent-prompt-webfetch-summarizer.md` (and similar isolated micro-agents) intentionally
hardcode user-specific epistemic preferences (scout mindset, observation/inference separation,
evidence weighting). This violates principle 2 (delegate to CLAUDE.md) because micro-agents
are isolated LLM calls that receive only their agent-prompt + task input -- no project context,
no CLAUDE.md. There is no CLAUDE_MD template variable to inject it. Inline is the only option.

## Quick start

```sh
# 1. Clone into ~/.tweakcc
git clone https://github.com/wassname/tweakcc-minimal ~/.tweakcc

# 2. Install Claude Code (native or npm)
# Native: https://claude.ai/download
# npm: npm install -g @anthropic-ai/claude-code

# 3. Apply tweaks + run full checks (template + runtime)
just apply

# 4. If state is corrupted, full reset + reinstall + apply + checks
just fresh

# 5. Install skills (optional, some tools converted to stub+skills)
mkdir -p ~/.claude/skills
ln -s $PWD/skills/* ~/.claude/skills
```

Backups at `out/<version>/native/{backup,backup.js,patched,patched.js}` (gitignored).

## Troubleshooting

### Lessons learned

1. Every template variable used in prompt body expressions (for example `${EXIT_PLAN_MODE_TOOL.name}`) must be declared in the file header `variables:` list.
2. Do not remove unknown template references blindly. First decide whether to (a) declare a missing variable in header, or (b) remove/replace an invalid reference. Keep semantics minimal and explicit.
3. `claude -p ping -v` is a marker check only. Real health check must parse `--output-format stream-json` and require `result.subtype == "success"`.
4. Run static template audit before runtime test. It catches undefined template symbols deterministically.

Template-error playbook:

1. Run `just apply` (it includes template audit + strict runtime ping).
2. If it fails with undefined symbol, inspect the file and classify:
	- **missing declaration**: symbol is valid and intended -> add it to header `variables:`
	- **invalid/offending reference**: symbol is bogus for that file -> remove/replace expression
3. Re-run `just apply` until both audits pass.

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

- `just fresh`

This removes legacy tweakcc backups, clears local `out/`, reinstalls Claude Code, patches the npm/global `cli.js`, and writes fresh backups to `out/<version>/`.

Use this as a recovery path, not the normal workflow. Normal day-to-day flow should stay:

- `just apply`

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

run `just apply` again. The apply script re-pins both `ccInstallationPath` and the `~/.local/bin/claude` symlink before patching.

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
| `system-reminder-plan-mode-is-active-5-phase.md` | Plan mode workflow (defers to CLAUDE.md) |
| `system-reminder-plan-mode-is-active-iterative.md` | Iterative plan mode variant |
| `system-prompt-tone-concise-output-detailed.md` | Output style (accuracy over validation) |
| `system-prompt-tone-concise-output-short.md` | Response length defaults |
| `system-prompt-hooks-configuration.md` | Hook event definitions (don't drop events) |
| `agent-prompt-webfetch-summarizer.md` | Epistemic preferences for isolated micro-agent |

~220 files untouched (already minimal, tool descriptions, agent/skill prompts loaded on-demand).

## What changed (vs stock prompts)

| Category | Files | What we did |
|----------|-------|-------------|
| Tool descriptions | todowrite, teammatetool, sendmessage, bash-git-commit, enterplanmode, task, readfile, websearch, ... | Compressed. Cut examples and patterns the model already knows. Kept schemas and tool-binding info. |
| Plan mode | plan-mode-5-phase, iterative, subagent, re-entry | Defer to CLAUDE.md for workflow. Provide minimal defaults if no project instructions exist. |
| Tone | tone-concise-output-detailed, tone-concise-output-short | Accuracy over validation. Disagree when warranted. No emojis, no time estimates. |
| WebFetch | tool-description-webfetch | Prefer skills/MCP for specific domains. Save to `evidence/` for research. |
| WebFetch summarizer | agent-prompt-webfetch-summarizer | Scout mindset, observation/inference separation, credence weighting. Inline because micro-agents don't see CLAUDE.md. |
| Verbose system prompts | hooks-config, learning-mode, insights-*, executing-actions, chrome-automation, skillify | Compressed. Kept structure, cut examples. |


## Links

- [tweakcc](https://github.com/Piebald-AI/tweakcc) | [CC system prompts source](https://github.com/Piebald-AI/claude-code-system-prompts)
- [Pi system prompt](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/src/core/system-prompt.ts) | [Armin's blog](https://lucumr.pocoo.org/2026/1/31/pi/)
- Other mods: [bl-ue/tweakcc-system-prompts](https://github.com/bl-ue/tweakcc-system-prompts) | [yansircc/tweakcc-prompts](https://github.com/yansircc/tweakcc-prompts) | [principled-claude-code](https://github.com/m0n0x41d/principled-claude-code)
- [Trail of Bits Claude Code Config](https://github.com/trailofbits/claude-code-config)
- [Internals](https://www.southbridge.ai/blog/claude-code-an-analysis)


## Appendix future work

- Patch vscode-bundled claude (snap: `~/snap/code-insiders/.../.local/share/claude/versions/X.Y.Z`)
- Auto-detect CC version bumps and run orphan check
