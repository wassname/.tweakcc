# tweakcc

Minimal system prompts for Claude Code. Customizations in `system-prompts/*.md`, stock reference in `stock-reference/`.

## Compression principles

1. **Trust the model** -- cut tutorials, examples, when-to-use lists. The model knows how to code.
2. **Defer to CLAUDE.md** -- say "follow CLAUDE.md conventions if present", don't prescribe workflow.
3. **Evidence over summaries** -- subagents return block quotes + links as primary output. Coordinators preserve them. No lossy telephone.
4. **Cut what doesn't earn its context cost** -- if removing a line hasn't caused a failure you've actually seen, cut it.
5. **Cheapest effective layer** -- enforce at: OS sandbox > deny rules > hooks > prompt text (last resort).

Review each prompt against: (1) model already knows this? Remove. (2) CLAUDE.md says this? Remove from system prompt. (3) Safety-critical? Keep, compress. (4) Tool-binding? Keep. (5) Proven behavioral shaping? Keep. (6) Context cost vs benefit? Prioritize always-loaded cuts.

## Context budget (21 custom files, -43%)

| Category | Stock | Custom | Reduction | Loading |
|----------|-------|--------|-----------|---------|
| System Prompts | ~13.7k | ~8.1k | -41% | Always |
| Tool Descriptions | ~15.1k | ~8.3k | -45% | Always |
| System Reminders | ~2.5k | ~2.5k | -- | Event-driven |
| Agent Prompts | ~24.5k | ~24.5k | -- | On-demand |

Always-loaded: ~16.4k words (down from ~28.8k stock). See `memory/compression-notes.md` for per-file rationale and remaining targets.

## How to edit

1. Edit `.md` files in `system-prompts/`
2. `just apply` -- restores clean binary, patches once, cleans up stock files, audits
3. Add new file stems to `CUSTOM_FILES` in `scripts/cleanup_stock_prompts.py`
4. Backticks in body must be escaped as `\`` (tweakcc parser requirement)
5. Frontmatter (name, description, ccVersion, variables) is restored by tweakcc from upstream. We only control body content.
6. `stock-reference/` has unmodified upstream prompts for diffing

**CRITICAL: system-prompts/ must only contain files we actively customize.** Stock files with `${VAR.property}` expressions become literal JS when patched back, causing ReferenceErrors. `cleanup_stock_prompts.py` deletes non-custom files.

**CRITICAL: `just apply` deletes `native-binary.backup` before patching.** Without this, tweakcc restores its stale internal backup and stacks patches (3x version lines, 1.2G binary).

**NEVER delete `DO_NOT_DELETE_patched_binaries/`**. Write-once archive, irreplaceable.

## What gets loaded when

Always: `system-prompt-*`, `tool-description-*` (highest compression value).
Event-driven: `system-reminder-*` (plan mode, tasks, hooks).
On-demand: `agent-prompt-*`, `data-*`, `skill-*`.
Within-file conditionals (`${VAR?trueText:""}`) are render-time, not file-level gates.

## Version upgrade runbook

Single-target: bun-installed npm binary. Each CC version gets a git tag.

### Phase 1: `just install <VERSION>`
Runs bun install, postinstall, backs up clean binary, updates config.json.

### Phase 2: `just extract`
Generates stock .md files to `stock-reference/`, restores clean binary. Commit baseline.

### Phase 3: Review upstream changes (JUDGMENT)
`git diff HEAD~1 -- stock-reference/` -- look for renamed/removed prompts, changed template vars, new compression targets.

### Phase 4: Write customizations (JUDGMENT)
Read stock in `stock-reference/<id>.md`, apply compression principles, write to `system-prompts/<id>.md`, add to CUSTOM_FILES. Don't override files that only differ by runtime var placeholders. Don't include `${VAR.property}` or `${FUNC()}` expressions in body text.

### Phase 5: `just apply`
Restores clean binary, patches once, cleans up, audits.

### Phase 6: `just smoke` (JUDGMENT)
Checks 1x tweakcc in version, canary "evidence" in webfetch description. If WRITE_TOOL crash: stock file leaked through. If canary missing: customization not applied.

### Phase 7: `just ship <VERSION>` then commit + tag
