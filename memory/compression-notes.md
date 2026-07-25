# Compression status

27 customizations on CC 2.1.219: **22,100 stock words -> 3,969 custom (-18,131, ~24k tokens)**.
Regenerate the numbers, don't trust this line:

```sh
c=0; s=0; for f in system-prompts/*.md; do st=$(basename "$f" .md)
  c=$((c+$(wc -w < "$f"))); s=$((s+$(wc -w < "stock-reference/$st.md"))); done
echo "stock $s -> custom $c (saved $((s-c)))"
```

## Compressed on 2.1.219 (new this version)

| prompt | stock | custom |
|---|---:|---:|
| system-prompt-coordinator-mode-orchestration | 2462 | 218 |
| tool-description-bash-git-commit-and-pr-creation-instructions | 1143 | 271 |
| tool-description-schedulewakeup-delay-and-reason-guidance | 829 | 200 |
| tool-description-artifact-publishing-and-update-guidance | 829 | 204 |
| tool-description-endconversation | 786 | 197 |
| system-prompt-persistent-memory-usage-and-writing-guidance | 679 | 224 |
| system-prompt-claude-in-chrome-browser-automation | 605 | 172 |

Biggest single win overall stays `tool-description-workflow` (2861 -> 277).

## Remaining candidates (uncustomized, 2.1.219)

| words | prompt | call |
|---:|---|---|
| 1106 | system-prompt-auto-mode-setup-proposal-generator | skipped: only loads during auto-mode setup, not per-turn |
| 630 | system-prompt-partial-compaction-instructions | worth doing; fires on every compaction |
| 605 | tool-description-designsync | skipped: tool unused here |
| 553 | system-prompt-repl-tool-usage-and-scripting-conventions | worth doing if the REPL tool is enabled |
| 498 | tool-description-croncreate | marginal |
| 490 | system-prompt-remote-plan-mode-ultraplan | skipped: remote plan mode unused |
| 487 | system-prompt-outcome-first-communication-style | check for conflict with CLAUDE.md voice rules before touching |

Everything else is under ~400 words; not worth the landing risk.

## Judgement calls worth revisiting

- `bash-git-commit`: stock said "NEVER commit unless the user explicitly asks"; ours defers to CLAUDE.md, which says commit often without being asked. Deliberate behavior change.
- `coordinator-mode-orchestration` cut 94% on the assumption teams are rarely used. Restore the phase table and worker-failure handling first if coordinator runs start misbehaving.
- `persistent-memory`: dropped the anti-deferral elaboration. If memory writes start drifting to end-of-conversation, restore that first.
- `schedulewakeup`: dropped `${SCHEDULE_WAKEUP_BASE_DESCRIPTION}` (banned template var) and restated the parameter contract inline from the sibling snooze prompt. Not confirmed against the runtime value.
- `artifact`: the watch block was a template conditional, so it is gone rather than conditional.
