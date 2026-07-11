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

## Upgrade: pick target -> `just install <V>` -> `extract` -> review -> customs -> `apply` -> `smoke` -> `ship <V>`

Target = highest `prompts-<V>.json` in tweakcc's GitHub `data/prompts/` (this is "latest supported"), NOT npm-latest CC. Check:
`curl -s https://api.github.com/repos/Piebald-AI/tweakcc/contents/data/prompts | jq -r '.[].name' | sort -V | tail`

1. `just install <V>` then `just extract`. Extract must print >0 prompts (else tweakcc lacks support for `<V>`).
2. Commit `stock-reference/` as a per-version baseline so the next upgrade's `git diff HEAD~1 -- stock-reference/` works.
3. Review + port (JUDGMENT): `git diff HEAD~1 -- stock-reference/`. A `CUSTOM_FILES` stem with no matching `stock-reference/<stem>.md` was removed upstream -> drop it from `cleanup_stock_prompts.py`. Fix any custom body that now states wrong behavior (a changed opt-in keyword, a flipped default). Frontmatter is upstream-controlled; only body content matters.
4. `just apply` (audits vars + upstream matches), then `just smoke`.

Gotchas (learned 2.1.156 -> 2.1.206):
- tweakcc 4.0.13 can't patch the cosmetic "(tweakcc)" version line into newer CC binaries, so `claude -v` shows 0 tweakcc lines. That is fine. The smoke canary ("evidence" in the webfetch description) is the real proof the prompt patch landed; smoke only fails on >1 version line (stacking).
- Do NOT blindly bump tweakcc for a big jump. 4.3.1 broke the 2.1.206 binary (ternary SyntaxError at `claude -v`). 4.0.13 is the pinned known-good. Only bump if extract yields 0 prompts, and re-run `smoke` plus `claude -v` to confirm the binary still starts.

See `just --list` and `memory/compression-notes.md`.
