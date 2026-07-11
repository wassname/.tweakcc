# tweakcc

Minimal system prompts for Claude Code. Edits in `system-prompts/`, stock baselines in `stock-reference/`.

## Principles

1. **Trust the model** -- cut tutorials, examples, when-to-use. It knows how to code.
2. **Defer to CLAUDE.md** -- say "follow CLAUDE.md conventions", don't prescribe workflow.
3. **Evidence-anchored** -- subagents produce block quotes + links as primary output; coordinators relay them intact, not re-summarized.
4. **Proven value only** -- if removing a line hasn't caused a failure you've seen, cut it.
5. **Cheapest layer** -- OS sandbox > deny rules > hooks > prompt text (last resort).

Review: (1) model knows this? Remove. (2) CLAUDE.md says this? Remove. (3) Safety-critical / tool-binding? Keep, compress. (4) Context cost justified? Cut always-loaded first.

## Editing

1. Edit `system-prompts/<id>.md`, add stem to `CUSTOM_FILES` in `scripts/cleanup_stock_prompts.py`
2. `just apply` -- restore clean binary, patch once, clean stock files, audit
3. Escape backticks as `\`` in body. Frontmatter is upstream-controlled.
4. Never include `${VAR.property}` expressions -- they become literal JS and crash.
5. `stock-reference/` has unmodified upstream for diffing.

## Guardrails

- **system-prompts/ = custom files only.** Stock files cause ReferenceErrors. `cleanup_stock_prompts.py` enforces this.
- **`just apply` deletes `native-binary.backup` first.** Prevents stacked patches (3x version, 1.2G binary).
- **Never delete `DO_NOT_DELETE_patched_binaries/`.** Write-once, irreplaceable.

## Upgrade: `just install <V>` -> `extract` -> review diffs -> write customs -> `apply` -> `smoke` -> `ship <V>`

Phases 3-4 need judgment: check `git diff HEAD~1 -- stock-reference/` for changed vars/prompts, apply principles above. See `just --list` and `memory/compression-notes.md` for details.
