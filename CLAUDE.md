# tweakcc

Minimal system prompts for Claude Code. Edits in `system-prompts/`, stock baselines in `stock-reference/`.

## Principles

1. **Trust the model** -- cut tutorials, examples, when-to-use. It knows how to code.
2. **Defer to CLAUDE.md** -- say "follow CLAUDE.md conventions", don't prescribe workflow.
3. **Evidence-anchored** -- subagents produce block quotes + links as primary output; coordinators relay them intact, not re-summarized.
4. **Preserve user intent across prompt churn** -- a removed or renamed stem is not evidence that its behavior is obsolete. Search history and port the intent to the replacement architecture.
5. **Proven value only** -- if removing a line hasn't caused a failure you've seen, cut it.
6. **Cheapest layer** -- OS sandbox > deny rules > hooks > prompt text (last resort).
7. **Never flatten a conditional.** If stock wraps text in `${VAR ? A : B}`, keep the branch, keep the interpolation, or drop both sides. Keeping one branch and stating it as fact is the worst outcome available: the result is not a shorter prompt, it is a confidently false one, and it costs words to boot.

Review: (1) model knows this? Remove. (2) CLAUDE.md says this? Remove. (3) Safety-critical / tool-binding? Keep, compress. (4) Context cost justified? Cut always-loaded first. (5) Does stock make this conditional? Then we may not state it flat.

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

For 2.1.283, run `just tweakcc-2-1-283` first. It builds the pinned prompt snapshot plus tweakcc PR #1011, which is required for the split native module layout in Claude Code 2.1.242+.

Target = highest `prompts-<V>.json` in tweakcc's GitHub `data/prompts/` (this is "latest supported"), NOT npm-latest CC. Check:
`curl -s https://api.github.com/repos/Piebald-AI/tweakcc/contents/data/prompts | jq -r '.[].name' | sort -V | tail`

1. `just install <V>` then `just extract`. Extract must print >0 prompts (else tweakcc lacks support for `<V>`).
2. Commit `stock-reference/` as a per-version baseline so the next upgrade's `git diff HEAD~1 -- stock-reference/` works.
3. Review + port (JUDGMENT): `git diff HEAD~1 -- stock-reference/`. Three things:
   a. A `CUSTOM_FILES` stem with no matching `stock-reference/<stem>.md` was removed upstream -> drop it from `cleanup_stock_prompts.py`.
   b. Fix any custom body that now states wrong behavior (a changed opt-in keyword, a flipped default). Frontmatter is upstream-controlled; only body content matters.
   b2. Audit every ported body against fresh stock for two bugs `check_landed.py` cannot see, because it checks landing and not content. FLATTENED CONDITIONAL: stock has `${VAR ? A : B}` and our body states one branch as fact. DROPPED CONSTRAINT: a prohibition, numeric limit, or safety carve-out in stock with no equivalent in ours. Fan this out (one subagent per few stems) and require a verbatim stock quote per finding; a finding without one is not a finding. This class survived three upgrades undetected and produced a false "you cannot wait more than 5 minutes" belief, see `RESEARCH_JOURNAL.md` 2026-08-08 (a).
   b3. Audit deletions for LOST USER INTENT before dropping any custom stem. Compare each candidate with freshly extracted same-version stock, then run `git log --all --follow -- system-prompts/<old-stem>.md` and read intentional edits since the last stock baseline. If upstream renamed or replaced the prompt, port the behavior to the current call path; do not preserve a dead filename or silently discard the behavior. Record every non-stock hunk and its replacement (or explicit retirement reason) in `slop/audits/`. An allowlist alone is not evidence that deletion is safe.
   b4. Audit executable prompts for USER-CONFLICT LANGUAGE with `rg -ni -C 2 'refus|copyright|piracy|pirate|download|guard|safe|safety|harm|malicious|censor|policy|classifier|sensitive|cyber|hack|exploit|bio|pathogen|machine learning|alignment|anthropic|lawsuit|legal|law|dual.?use|authorization context|detection evasion' stock-reference/{agent-prompt,system-prompt,system-reminder,tool-description}-*.md`. Classify every relevant hit as topic/content restriction or operational integrity. Replace local topic-based restrictions with faithful help under the user's stated context. Retain controls for file loss, credentials, publication authority, and prompt injection. A request for quotation, raw content, or download must not become a summary; quote the whole relevant passage with at least one complete sentence before and after the key sentence, preserve spelling, attribute it, and give the source URL.
   c. Compress NEW large stock prompts (`tool-description-*`, `system-prompt-*`) per the Principles above. Big jumps add many prompts; the goal is to strip, not just preserve. "I reviewed them" is not an output: rank every uncustomized stem by word count and show the top 10 as a table with a decision per row (compress / skip + why). Anything >600 words needs a stated reason to skip. Status lives in `memory/compression-notes.md`.
4. `just apply` (audits vars + upstream-matches, hard-fails via `check_landed.py` if any customization did not patch, then hard-fails via `verify_in_binary.py` if any custom text is missing from the binary bytes), then `just smoke`.
5. Print the proof block below. The run is not finished until you do.

Ranking command for 3c (only these two prefixes: `skill-*` and `data-*` are loaded on demand, so their size is not context you pay for every turn):
```sh
for f in stock-reference/tool-description-*.md stock-reference/system-prompt-*.md; do
  s=$(basename "$f" .md); [ -f "system-prompts/$s.md" ] || echo "$(wc -w < "$f") $s"
done | sort -rn | head -12
```

## VERY IMPORTANT -- DO NOT SKIP: end every run with the proof block

Agents routinely skip this and report "all landed" or "much shorter now" from a single canary, from tweakcc's own log, or from nothing at all. None of that is proof: tweakcc says "applied" for prompts it silently failed to match, and `just smoke` exercises ONE prompt live. Claims are cheap; the artifacts below are hard to fake because they are copied out of files the user can open.

The last thing in your reply must be these four items, in this order. A reply missing any of them is an incomplete run, no matter how much work happened.

**1. Landing table** -- paste `out/verify.log` verbatim, all rows, no elision.

```
prompt                                    probes  ours  stock
tool-description-webfetch                      8     4      3
...
OK: all 27/27 customizations found in binary bytes
```

- `ours` = hits for a distinctive phrase from our body. **0 = did not land**, whatever tweakcc reported.
- `stock` = hits for a stock phrase we cut. >0 is expected (the binary holds duplicate copies) and is informational.
- `probes` = greppable fragments found. **0 probes proves nothing** and must be checked by hand.

**2. Savings table** -- per prompt touched, `stock -> custom` words and the delta, plus the total across all `CUSTOM_FILES`. Compute it, do not estimate it.

**3. Quotes for every behavioral change** -- for each body you edited or added, one verbatim quote from `stock-reference/<stem>.md` and the line you replaced it with. This is what catches a compression that silently dropped a constraint. If you changed nothing, say so.

**4. What is NOT verified** -- name the prompts that are byte-verified only (not exercised live), any `probes 0` rows, anything you could not land and why, and any behavior you deliberately changed (e.g. deferring to CLAUDE.md where stock said otherwise) so the user can veto it.

Do not paraphrase these into prose. Tables and quotes, or it did not happen.

Lazy tells, all of which mean the run is unfinished: "all customizations landed" with no table; "verified" without saying byte-verified vs live; a savings number that is round or estimated rather than computed; "reviewed the new prompts" with no ranked table; "should work" / "looks good" anywhere. `out/verify.log` only exists after a real `just apply`, so pasting it is the cheapest honest move.

Gotchas (learned 2.1.156 -> 2.1.206):
- Landing is NOT guaranteed and NOT the same as "applied". tweakcc matches each stock prompt by a whole-prompt regex; if upstream text drifted anywhere in that span, the match silently misses and the binary keeps stock. `just apply` now fails on this (`check_landed.py` reads tweakcc's own "Could not find" report). The smoke canary only checks ONE prompt, so it is necessary but not sufficient. If a prompt genuinely cannot land on this version (workflow on 2.1.206: 4.0.13 misses it, 4.3.1 breaks the binary), drop it from `CUSTOM_FILES` with a note rather than ship a false claim.
- tweakcc 4.0.13 can't patch the cosmetic "(tweakcc)" version line into newer CC binaries, so `claude -v` shows 0 tweakcc lines. That is fine. Smoke only fails on >1 version line (stacking).
- tweakcc pin tracks the CC version. 4.0.13 was known-good through 2.1.206 but is INADEQUATE on 2.1.219 (extracts only 136/610 prompts, silently missing all tool-description-*/system-prompt-* categories, so nothing lands). 4.3.2 is the known-good pin for 2.1.219 (extracts all 610, boots fine; 4.3.1 booted-broken with a ternary SyntaxError, 4.3.2 fixed it). Trigger to bump: `just extract` yields 0 prompts OR the extraction is missing tool-description-*/system-prompt-* stems. After any bump re-run `apply` + `smoke` + `claude -v` to confirm the binary still starts. 4.3.x also needs `-y` on `--apply` (recipes already pass it).

See `just --list` and `memory/compression-notes.md`.
