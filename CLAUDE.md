# tweakcc-minimal

Minimal system prompts for Claude Code. Edits live in `system-prompts/*.md`.

## Design principles

Sources: [Pi system prompt](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/src/core/system-prompt.ts), [Pi blog post](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/), [Armin on Pi](https://lucumr.pocoo.org/2026/1/31/pi/), [Trail of Bits config](https://github.com/trailofbits/claude-code-config), [arch](https://www.southbridge.ai/blog/claude-code-an-analysis)

1. **Trust the model** -- frontier models know how to code; provide context and tools, not tutorials. Pi's entire prompt is ~1k tokens.
2. **Delegate workflow** -- CLAUDE.md/AGENTS.md own conventions, not the system prompt
3. **Disposability** -- cut anything that doesn't earn its context-window cost
4. **Sandbox over guardrails** -- real security = OS-level sandbox (bubblewrap/seatbelt via `/sandbox`) + deny rules + devcontainers, not verbose prompt text. Trail of Bits pairs `--dangerously-skip-permissions` with layered defense: sandbox + deny rules + ephemeral containers.
5. **Hooks over prompts** -- "NEVER use rm -rf" in a prompt can be forgotten; a PreToolUse hook fires every time.
6. **Cheapest effective layer** -- enforce at: OS sandbox > deny rules > hooks > prompt text (last resort)

## Review methodology: 6 dimensions

| # | Dimension | Question | If yes |
|---|-----------|----------|--------|
| 1 | Model-knows-this | Would the model do this without being told? | Remove |
| 2 | CLAUDE.md overlap | Is the user's CLAUDE.md already saying this? | Remove from system prompt |
| 3 | Safety-critical | Would removing this cause dangerous behavior? | Keep, compress |
| 4 | Tool-binding | Necessary for the tool to function? | Keep |
| 5 | Behavioral shaping | Meaningfully changes default behavior? | Keep if proven |
| 6 | Context cost | How many chars? Always-loaded? | Prioritize cuts in always-loaded |

Heuristic: if removing a line would cause a failure mode you've actually seen, keep it. If it's "just in case", cut it.

## What gets loaded when (CC 2.1.63)

Source: Southbridge Research reconstructed code (inferred, not decompiled). Treat thresholds as approximate.

**Prompt assembly priority** (lower priority truncated first under context pressure):
1. Base prompt (~2KB) > 2. Model adaptations > 3. CLAUDE.md (~5-50KB) > 4. Git context (~1-5KB) > 5. Directory > 6. Tools (~10KB+)

**Always loaded:**
- `system-prompt-*` core behavioral files
- `tool-description-*` for available tools (incl. MCP schemas as serialized JSON)
- Monolithic + sub-files both loaded by tweakcc; empty monolithic ones to avoid duplication

**Event-driven (injected per-turn on condition):**
- `system-reminder-plan-mode-*` -- when plan mode active
- `system-reminder-team-*` -- when team/swarm mode active
- `system-reminder-todo-*`, task nudges -- periodic / on task events
- File events, hook outcomes, token/budget warnings -- per-turn

**On-demand (loaded at spawn/invocation):**
- `agent-prompt-*` -- loaded when that agent type spawned
- `data-*`, `skill-*` -- referenced on demand

**Compaction**: triggers at 100k tokens OR 200 messages OR $5 cost. Skipped if <50 messages. Summarizes non-preserved messages via LLM call.

**Context budget:**

| Category | Stock words | tweakcc words | Reduction | Loading |
|----------|-------------|---------------|-----------|---------|
| System Prompts | ~4.5k | ~3.7k | -18% | Always (Priority 1) |
| Tool Descriptions | ~6.3k | ~3.8k | -40% | Always (Priority 6) |
| System Reminders | ~1.7k | ~1.7k | -- | Event-driven |
| Agent Prompts | ~6.9k | ~6.9k | -- | On-demand (spawn) |

Total always-loaded: ~7.5k words (down from ~10.8k stock).
On-demand (untouched): Data ~154k chars, Skills ~45k chars, Agent Prompts ~69k chars.

**Frontmatter is upstream-controlled**: `tweakcc --apply` restores YAML headers (name, description, ccVersion, variables) from CC. We only control the body content.

## How to edit

1. Edit `.md` files in `system-prompts/`
2. Re-apply: `npx tweakcc --apply`
3. Files use YAML frontmatter in HTML comments + `${VARIABLE}` template interpolation
4. Backticks in body must be escaped as `\`` (tweakcc parser requirement)
5. Don't delete files; empty the content to disable (tweakcc expects files to exist)
6. Header-only files (just `<!-- -->`) effectively disable that prompt piece

## File naming conventions

- `system-prompt-*` -- core behavioral, always loaded
- `system-reminder-*` -- event-driven (plan mode, task nudges, file events, hooks)
- `tool-description-*` -- loaded with tool schemas
- `agent-prompt-*` -- loaded when agent type spawned
- `data-*` -- reference data, on-demand
- `skill-*` -- skill definitions, on-demand