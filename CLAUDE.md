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
3. Review + port (JUDGMENT): `git diff HEAD~1 -- stock-reference/`. Three things:
   a. A `CUSTOM_FILES` stem with no matching `stock-reference/<stem>.md` was removed upstream -> drop it from `cleanup_stock_prompts.py`.
   b. Fix any custom body that now states wrong behavior (a changed opt-in keyword, a flipped default). Frontmatter is upstream-controlled; only body content matters.
   c. Scan NEW large always-loaded stock prompts (`tool-description-*`, `system-prompt-*`) for compression targets per the Principles above. Big jumps add many prompts; the goal is to strip, not just preserve. Candidates and status live in `memory/compression-notes.md`.
4. `just apply` (audits vars + upstream-matches, AND hard-fails via `check_landed.py` if any customization did not patch), then `just smoke`.

Gotchas (learned 2.1.156 -> 2.1.206):
- Landing is NOT guaranteed and NOT the same as "applied". tweakcc matches each stock prompt by a whole-prompt regex; if upstream text drifted anywhere in that span, the match silently misses and the binary keeps stock. `just apply` now fails on this (`check_landed.py` reads tweakcc's own "Could not find" report). The smoke canary only checks ONE prompt, so it is necessary but not sufficient. If a prompt genuinely cannot land on this version (workflow on 2.1.206: 4.0.13 misses it, 4.3.1 breaks the binary), drop it from `CUSTOM_FILES` with a note rather than ship a false claim.
- tweakcc 4.0.13 can't patch the cosmetic "(tweakcc)" version line into newer CC binaries, so `claude -v` shows 0 tweakcc lines. That is fine. Smoke only fails on >1 version line (stacking).
- tweakcc pin tracks the CC version. 4.0.13 was known-good through 2.1.206 but is INADEQUATE on 2.1.219 (extracts only 136/610 prompts, silently missing all tool-description-*/system-prompt-* categories, so nothing lands). 4.3.2 is the known-good pin for 2.1.219 (extracts all 610, boots fine; 4.3.1 booted-broken with a ternary SyntaxError, 4.3.2 fixed it). Trigger to bump: `just extract` yields 0 prompts OR the extraction is missing tool-description-*/system-prompt-* stems. After any bump re-run `apply` + `smoke` + `claude -v` to confirm the binary still starts. 4.3.x also needs `-y` on `--apply` (recipes already pass it).

See `just --list` and `memory/compression-notes.md`.
