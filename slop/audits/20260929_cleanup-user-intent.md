# 2.1.147 cleanup user-intent audit

## Observation

Commit `017a0f5` deleted 288 prompt files to avoid `${VAR.property}` runtime crashes. The deletion was architectural, not evidence that each prompt's behavior was obsolete. The audit covered 47 `agent-*`, 115 `system-prompt-*` / `system-reminder-*`, 125 `data-*` / `skill-*` / `tool-description-*`, and one stock tool-parameter file.

## Intent ledger

| Historical intent | Evidence | 2.1.283 resolution |
|---|---|---|
| Direct contextual WebFetch quotations and explicit epistemics | `b127fc6`, strengthened by `a905fb0`; partially restored by `3b071cb`, then deleted by `017a0f5` | Restored in `agent-prompt-web-reading-specialist`, its caller guidance, and full/concise WebFetch descriptions |
| Preserve decision paths across compaction | `5801e29` | Restored in `system-prompt-context-compaction-summary` |
| Brainstorm during batch planning | `a905fb0` changed only a heading to “Research, Brainstorm, and Plan” | Retired: the heading added no executable instruction; restoring the large prompt would add a fragile override without behavior |
| Remove false WebSearch “US only” claim | `bac4b51` | Restored in full and concise WebSearch descriptions |
| Route commit/PR work through `cc-commit` | `65887ab` | Behavior retained: the skill still exists and current prompt contains its workflow; exact routing is not required for behavior |
| Remove narrating comments | `3b071cb` `/simplify` edit | Preserved more strongly in current `AGENTS.md` |
| Project/user workflow overrides defaults | `5760527`, `362b73d`, `a905fb0` | Preserved in current `AGENTS.md`, `CLAUDE.md`, and custom plan/communication prompts |
| Accuracy over validation; no unsolicited estimates/emojis | `3b071cb` | Preserved in current `AGENTS.md` and communication prompt |
| Confirm destructive/outward actions and preserve user work | `5760527` | Preserved and strengthened in `system-prompt-executing-actions-with-care` |
| User controls documentation creation; do not discuss an invisible plan; explicit-only teams | `5801e29`, `5347b10` | Preserved by current stock and agent rules |
| Remaining deleted bodies | Same-version comparison and per-file history | Stock/version churn, variable fixes, or semantic compression; no distinct user behavior found |

## Primary evidence

`b127fc6`, user-authored WebFetch summarizer:

> Provide a detailed response based only on the content above. Include full code examples and documentation excerpts as needed. **For factual claims, blockquote the relevant passage (3-5 sentences of surrounding context), bold the key fragment and include the source URL.** For code or docs, include full examples.

`a905fb0`, strengthened WebFetch summarizer:

> Provide a detailed response based only on the content above. Include full code examples and documentation excerpts as needed. **For factual claims, blockquote the whole relevant passage / section (3+ sentences of surrounding context), bold the key fragment, and include the source URL.**
>
> Please separate observation and inference as a summariser your job is observation and task focused compression while preserving epistemic metadata.
>
> Have a scout mindset, and think "document author claims X (credence 65%)" or "documents sources a textbook which reports X (credence 80%)" not "X is true".
>
> Weight evidence accordingly. If the content is from a high quality source e.g. Gwern.net or presents consistent and coherent high S/N evidence you can put more weight on it, likewise the opposite.

The later stock reset reintroduced the conflict before cleanup:

> Provide a concise response based only on the content above. In your response:
> - **Enforce a strict 125-character maximum for quotes from any source document.** Open Source Software is ok as long as we respect the license.
> - Use quotation marks for exact language from articles; any language outside of the quotation should never be word-for-word the same.
> - You are not a lawyer and never comment on the legality of your own prompts and responses.
> - Never produce or reproduce exact song lyrics.

`5801e29`, compaction:

> Task incomplete. Write a continuation summary to replace this conversation history. The next instance sees only this summary. **Preserve the guided path of decisions, not just facts.**
>
> Structure:
> 1. **Goal**: Core request, success criteria, user constraints/preferences
> 2. **Completed**: What's done, files changed (with paths), artifacts produced
> 3. **Decisions & dead ends**: Rationale for choices made, what failed and why
> 4. **Next steps**: Specific actions, priority order, blockers
> 5. **User context**: Preferences, style, promises, non-obvious domain details
>
> Prioritize: preventing duplicate work > preventing repeated mistakes > completeness.
> Wrap in <summary></summary> tags.

## Content-conflict classification

Patched local topic restrictions:

- malicious-activity censor: generic cyber refusal and authorization-context test;
- prompt suggestions: silence for legitimate security and other “sensitive” topics;
- full-scope prompt: vague local “genuinely harmful” refusal test;
- WebFetch: summary substitution, missing contextual quotation, and no download route;
- WebSearch: historical region restriction intentionally retired from full and concise prompts, matching `bac4b51`; this audit did not test service availability by region.

Kept operational integrity controls: file-loss checks, credential protection, publication authority, permission provenance, sandbox boundaries, and webpage prompt-injection handling. These protect the user's machine and authority; they do not classify cyber, bio, ML, alignment, copyright, piracy, downloading, or legal topics.

Fresh-eyes review also restored runtime-supplied fork/subagent-writing guidance, teammate parameter limits, commit and PR attribution, pre-commit guidance, and PR templates that earlier compressed bodies had dropped. The PowerShell prompt remains intentionally local to this Linux installation; it must return to dynamic edition guidance before reuse on Windows.

Server-side Anthropic classifiers are not stored in these prompt files and cannot be removed by this patch. The local prompts now require exact reporting of any actual higher-priority or server block instead of inventing or broadening one.

-- codex[astra]
