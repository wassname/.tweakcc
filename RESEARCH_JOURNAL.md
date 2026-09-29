# tweakcc research journal

Lab notes on compressing Claude Code's system prompts. Oldest first, append at the bottom.

## 2026-08-08 (a) -- a compressed prompt taught the model a wait limit that does not exist

wassname reported bad behavior on the current build, specifically "weird things like background tasks" and an agent claiming it could not wait more than five minutes for background work. This entry records what the session logs show, what the binary actually enforces, and one bug in our own compression that explains the belief.

### The five-minute ceiling is not real

The runtime clamp on `ScheduleWakeup`, the tool that sets how long the model sleeps before its next turn, comes straight out of the patched binary:

```
delaySeconds: v.number().describe("Seconds from now to wake up. Clamped to [60, 3600] by the runtime. Required unless `stop` is true.")
...
function Xey(e){ ... let r=Math.max(Y7r,Math.min(Opo,t)) ... }
var zey,Y7r=60,Opo=3600,Key=1200,Yey=1;
```

Source: `strings node_modules/@anthropic-ai/claude-code/bin/claude.exe | grep delaySeconds`. `Y7r` is the lower bound in seconds and `Opo` the upper, so the enforced range is 60 to 3600 seconds.

Background Bash tasks have no such bound at all. Matching every `run_in_background: true` tool call against the `<task-notification>` that later reported its completion, across all sessions since 2026-07-25:

| duration | background tasks |
| --- | --- |
| under 1 min | 21 |
| 1 to 5 min | 42 |
| 5 to 15 min | 67 |
| 15 to 60 min | 77 |
| over 1 hour | 78 |

Table 1. Wall-clock time from launch to completion notification, 285 matched tasks. Source: ` out/session_bgdur.log `, produced by ` scripts/session_audit/dur.py `. The longest single task ran 3953 minutes, about 66 hours.

So 222 of 285 background tasks, 78 percent, already ran past five minutes, and the model was notified about every one of them.

### Where the belief came from

Upstream branches this guidance on a variable named `PROMPT_CACHE_TTL_CLASSIFICATION`, which encodes how long the session's prompt cache lives. The true branch says there is no cliff to pace around:

> This session's requests use a 1-hour Anthropic prompt-cache TTL, so effectively every allowed delay (the runtime clamps to [60, 3600]) wakes up with your conversation context still cached. There is no cache cliff inside that range to pace around

The false branch says the opposite:

> This session's requests use the default 5-minute Anthropic prompt-cache TTL. Sleeping past 300 seconds means the next wake-up reads your full conversation context uncached

Source: ` stock-reference/tool-description-schedulewakeup-delay-and-reason-guidance.md ` lines 16 to 39.

Our compressed body flattened the three-way conditional into one unconditional sentence carrying only the five-minute branch:

> On a 5-minute prompt-cache TTL prefer 270s over 300s, and never schedule extra wakeups just to keep the cache warm.

Source: ` system-prompts/tool-description-schedulewakeup-delay-and-reason-guidance.md ` at commit 287b725, line 14.

My first read was that this line was the direct cause, and checking it dropped my confidence a lot. `ScheduleWakeup` has been called four times in the entire log, on 2026-07-05, 2026-07-25 twice, and 2026-08-01, with delays of 1500, 1500, 1800 and 2700 seconds. None were clamped. A prompt that is almost never exercised cannot be doing much work, so I now think it is *unlikely*, maybe 0.15, that this line is the main driver, though it is still wrong and still worth fixing.

The behavior actually lives on the Bash tool. Grouping every "Command timed out" error by the command that produced it:

```
top timed-out commands:
     9  sleep 115; sleep 110; echo waiting
     4  sleep 115; sleep 100; echo waiting
     4  sleep 115; sleep 60; ls data/05_models/evals/20260804_adaptllm-validat
     4  sleep 120; echo waited
by leading binary:
   257  sleep
    46  cd
```

Source: ` scripts/session_audit/tmocmd.py `. Of 322 timeouts at the 120 second default, 257 are `sleep`, and 33921 of 34000-odd Bash calls pass no `timeout` at all.

`sleep 115; sleep 110` is the tell. The model is splitting one wait into sub-two-minute pieces to stay under a ceiling it half-remembers, then the pieces sum past the ceiling and the whole call dies anyway. A separate group of 16 calls requested timeouts of 840000 to 1900000 ms and were silently clamped to the 600000 ms maximum, reported only as "Command timed out after 10m 0s" with no mention that the request had been reduced.

Splitting that by era separates a long-standing problem from a new habit:

```
metric           pre <2026-07-25       post   per 1k Bash calls
bash_calls                12918      22996
chained_sleep                 0         62   0.00 -> 2.70
sleep_timeout                98        159   7.59 -> 6.91
```

Table 2. `chained_sleep` counts Bash commands matching `sleep N; sleep M`; `sleep_timeout` counts timeout errors on commands beginning with `sleep`. Source: ` out/session_sleepchain.log `, produced by ` scripts/session_audit/sleep_chaining.py `.

My read: the timeouts themselves are old news, since the rate per thousand Bash calls did not move and if anything fell slightly. The chaining workaround is new, and I think that *almost certain*, since zero occurrences in 12918 prior Bash calls against 62 in 22996 later ones is not a sampling artifact at any reasonable prior. Something after 2026-07-25 taught the model to split a wait into sub-two-minute pieces, which is a workaround for a ceiling rather than a fix for one, and it does not even work because the pieces sum past the limit.

I cannot say which of the three simultaneous changes did it. The prompt line quoted above is a candidate but a weak one given `ScheduleWakeup` sees four calls in the whole log. My best guess, held loosely at maybe 0.5, is that this is opus-5 behavior rather than our compression, because the habit shows up in Bash where we customize nothing about timeouts. The correct moves, `run_in_background: true` for an unbounded wait and an explicit `timeout` up to 600000 ms for a bounded one, are both available and both under-used.

I call this failure mode a hardcoded branch: stock text is conditional on a template variable, and the compression keeps one branch and drops the condition. It is worse than ordinary over-compression because the result is not a thinner prompt, it is a confidently wrong one. Two more instances turned up in the same pass, both in the Agent tool usage notes, where stock's instruction not to poll a background agent and its "Don't race" paragraph forbidding invented results were dropped with nothing in their place.

### The performance complaint is confounded and this does not explain it

Tool-call error rates across every session file, split at the upgrade:

```
pre  (opus-4-8 / 2.1.206):  22664 tool calls,  959 errors, 4.23%  (19 days)
post (opus-5 / 2.1.219):    34577 tool calls, 1245 errors, 3.60%  (15 days)
```

Source: ` out/session_scan.log `, produced by ` scripts/session_audit/scan_sessions.py `. Sleep-command frequency and notification volume were flat over the same split.

Three things changed on 2026-07-25 at once: the model went from opus-4-8 to opus-5, Claude Code went from 2.1.206 to 2.1.219, and commit fa917b8 compressed seven more always-loaded prompts. My read: no split of this observational data can attribute the slowdown, and I would not update much on any before-and-after comparison drawn from it. The clean test is available and cheap, since ` DO_NOT_DELETE_patched_binaries/2.1.219/native/original ` is unpatched 2.1.219, so running the same task on patched and unpatched holds model and harness fixed and varies only our prompts.

### Next

Fixed all three bodies and re-applied; `out/verify.log` shows 27 of 27 landed and byte-verified, and the smoke canary passes live. A background agent is auditing the remaining 24 customized bodies for the same hardcoded-branch pattern.

The lesson worth carrying forward is that a compression which drops a conditional is not a smaller prompt, it is a false one, and only a diff against the stock branch structure catches it.

## 2026-09-29 -- Split native modules need a module-aware prompt patcher

This entry records why the first Claude Code upgrade attempt gave a false positive and what made the final build auditable.

The byte verifier reported:

> OK: all 15/15 customizations found in binary bytes

Source: `out/verify.log`, produced by `just apply` against Claude Code 2.1.283 with tweakcc prompt snapshot commit `871ed33e` merged with PR #1011 head `deb4839`.

The live smoke test reported:

> 2.1.283 (Claude Code)
>
> For evidence-grade research (need full text, blockquotes, save to disk), save the page to a file with bash instead

Source: `out/smoke.log`, produced by `just smoke`; the second line is unique to the customized WebFetch prompt.

Interpretation: my read is that prompt application is verified with high confidence. The byte check covers every retained custom prompt, and the live canary shows that Claude serves one of those patched descriptions at runtime. The other tweakcc user-interface patches still report no match, so this evidence does not support claims about them.

The takeaway is to require module-aware repacking and byte checks for every split-native Claude Code upgrade.

-- codex[astra]

## 2026-09-29 -- Prompt cleanup had dropped user intent

This entry records the historical audit of prompt files removed during the clean architecture migration.

The direct-quotation behavior existed before cleanup:

> Provide a detailed response based only on the content above. Include full code examples and documentation excerpts as needed. For factual claims, blockquote the relevant passage (3-5 sentences of surrounding context), bold the key fragment and include the source URL. For code or docs, include full examples.

Source: `system-prompts/agent-prompt-webfetch-summarizer.md` at commit `b127fc6`.

The cleanup later removed the prompt:

> 017a0f5 Upgrade to CC 2.1.147: clean prompt architecture, fix WRITE_TOOL crash
>
> system-prompts/agent-prompt-webfetch-summarizer.md | 26 deletions

Source: `git show --stat 017a0f5 -- system-prompts/agent-prompt-webfetch-summarizer.md`.

The current binary verifier reports:

> OK: all 24/24 customizations found in binary bytes

Source: `out/verify.log`, produced by the final `just apply`. The live test also returned the current customized WebFetch evidence line; source: `out/smoke.log`.

Interpretation: my read is that the direct-quotation regression is *almost certain*. The old behavior is explicit in git history, the cleanup deleted its only isolated-agent prompt, and the replacement architecture originally lacked an equivalent. The current patch restores it in the web-reading agent, its caller guidance, and both WebFetch descriptions. The audit also restored decision-path compaction and removed local topic-based refusal language. Server-side provider classifiers remain outside this binary.

The durable lesson is to compare every cleanup candidate with same-version stock and its full history before deleting it.

-- codex[astra]
