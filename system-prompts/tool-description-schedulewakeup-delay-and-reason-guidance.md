<!--
name: 'Tool Description: ScheduleWakeup delay and reason guidance'
description: >-
  Extends the ScheduleWakeup tool description with no-op reporting,
  prompt-cache-aware delay selection, and concise reason-field guidance
ccVersion: 2.1.242
variables:
  - SCHEDULE_WAKEUP_BASE_DESCRIPTION
  - PROMPT_CACHE_TTL_CLASSIFICATION
-->
Schedules when you resume work in /loop dynamic mode. Pass the same /loop prompt back via \`prompt\` each turn so the next firing repeats the task; for an autonomous loop with no user prompt, pass the literal sentinel \<\<autonomous-loop-dynamic\>\> as \`prompt\`. To end the loop, call with \`stop: true\` and omit every other field.

\`delaySeconds\` is clamped by the runtime to [60, 3600], so don't clamp yourself. Any delay in that range is fine; there is no shorter ceiling, and a longer wait is just the next wakeup re-arming. Idle ticks: 1200-1800s. Do NOT poll for background work you started, since you are re-invoked automatically when harness-tracked work finishes. When polling external state the harness cannot notify you about (a CI run, a deploy, a remote queue), match the delay to how fast that state changes.

Cache cost, if it matters: subscriber sessions hold context for an hour (unless usage overage drops it to five minutes), so nothing in [60, 3600] is normally a cliff; API-key, Bedrock and Vertex sessions hold it for five minutes, where 270s beats 300s and 1200s+ amortizes the miss. Never schedule extra wakeups just to keep the cache warm or try to predict an overage transition.

\`noop: true\` if nothing changed, \`false\` if something happened worth keeping; omit it when stopping. \`reason\`: one short specific sentence on what you chose and why, shown to the user.
