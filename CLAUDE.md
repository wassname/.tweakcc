# tweakcc-minimal

Minimal system prompts for Claude Code. Edits live in `system-prompts/*.md`.

## Design principles

Sources: [Pi system prompt](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/src/core/system-prompt.ts), [Pi blog post](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/), [Armin on Pi](https://lucumr.pocoo.org/2026/1/31/pi/), [Trail of Bits config](https://github.com/trailofbits/claude-code-config)

1. **Trust the model** -- frontier models know how to code; provide context and tools, not tutorials. Pi's entire prompt is ~1k tokens.
2. **Conditional inclusion** -- only include instructions for tools/capabilities available in this session
3. **Lazy-load** -- reference docs by path, don't embed; model reads on-demand
4. **Delegate workflow** -- CLAUDE.md/AGENTS.md own conventions, not the system prompt
5. **Disposability** -- cut anything that doesn't earn its context-window cost
6. **Sandbox over guardrails** -- real security = OS-level sandboxing (bubblewrap/seatbelt) + hooks at decision points, not verbose prompt text saying "NEVER do X". Trail of Bits runs `--dangerously-skip-permissions` + sandbox + deny rules. Pi runs full YOLO mode.
7. **Hooks over prompts** -- "NEVER use rm -rf" in a prompt can be forgotten; a PreToolUse hook blocking it fires every time. Hooks = structured prompt injection at the right moment.
8. **Skills over MCP descriptions** -- MCP server schemas dump 13-18k tokens into always-loaded context. Move less-used tools to skills (on-demand loading). Symlink `skills/` to `~/.claude/skills/`.

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

**Always loaded (every session):**
- `system-prompt-*` core behavioral files
- `tool-description-*` for available tools:
  - Always: Bash (+ sub-files), Read, Edit, Write, Glob, Grep, Agent/Task, AskUserQuestion, EnterPlanMode, ExitPlanMode, TodoWrite/TaskCreate/TaskList/TaskUpdate
  - Conditional: TeammateTool, SendMessageTool, TeamDelete (swarm only), Computer (computer use), Chrome (browser MCP)

**Per-mode:** `system-reminder-plan-mode-*`, `system-reminder-team-*`, `system-reminder-todo-*`

**On-demand:** `agent-prompt-*`, `data-*`, `skill-*`

**Context budget:**

| Category | Files | Stock chars | Loading |
|----------|-------|-------------|---------|
| Tool Descriptions | 71 | 63k | Always (biggest cost) |
| System Prompts | 52 | 45k | Always |
| System Reminders | 38 | 17k | Per-mode |
| Data | 25 | 154k | On-demand |
| Agent Prompts | 28 | 69k | On-demand |
| Skills | 7 | 45k | On-demand |

Note: CC 2.1.53+ split monolithic tool descriptions into granular sub-files. BOTH are loaded by tweakcc, so empty the monolithic ones to avoid duplication.

## How to edit

1. Edit `.md` files in `system-prompts/`
2. Re-apply: `npx tweakcc --apply`
3. Files use YAML frontmatter in HTML comments + `${VARIABLE}` template interpolation
4. Backticks in body must be escaped as `\`` (tweakcc parser requirement)
5. Don't delete files; empty the content to disable (tweakcc expects files to exist)
6. Header-only files (just `<!-- -->`) effectively disable that prompt piece

## File naming conventions

- `system-prompt-*` -- core behavioral, always loaded
- `system-reminder-*` -- mode-specific (plan mode, learning mode)
- `tool-description-*` -- loaded with tool schemas
- `agent-prompt-*` -- loaded when agent type spawned
- `data-*` -- reference data, on-demand
- `skill-*` -- skill definitions, on-demand
