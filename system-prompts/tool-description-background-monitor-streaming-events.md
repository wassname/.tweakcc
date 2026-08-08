<!--
name: 'Tool Description: Background monitor (streaming events)'
description: >-
  Describes the background monitor tool that streams stdout events from
  long-running scripts as chat notifications, with guidelines on script quality,
  output volume, and selective filtering
ccVersion: 2.1.119
variables:
  - BACKGROUND_TASKS_DISABLED
-->

Start a background monitor that streams events from a long-running script. Each stdout line becomes a notification. Events arrive on their own schedule and are not replies from the user, even if one lands while you are waiting for an answer.

Pick by notification count:
- One ("tell me when X is ready"): a Bash command that exits when the condition is true, e.g. \`until grep -q "Ready in" dev.log; do sleep 0.5; done\` -- run it in the background if that parameter exists, otherwise foreground. One notification, ends in seconds.
- Streaming: Monitor with an unbounded command (tail -f, inotifywait -m, polling loop)

Coverage: silence is not success. Your filter must match every terminal state, not just the happy path. A filter that greps only the success marker stays silent through a crashloop, a hang, or an unexpected exit, and that silence looks identical to "still running". Before arming, ask whether the filter would emit anything if the process crashed right now. Poll intervals: 30s+ for remote APIs (rate limits), 0.5-1s for local checks. Every pipe stage must flush per line or matches sit in the buffer unseen: \`grep\` needs \`--line-buffered\`, \`awk\` needs \`fflush()\`, \`head\` cannot flush at all.

Exit ends the watch (exit code is reported); timeout kills it; monitors that produce too many events are stopped automatically, so restart with a tighter filter. A silent monitor may have been stopped rather than still watching. Set \`persistent: true\` for session-length watches (PR monitoring, log tails); the monitor runs until you call TaskStop or the session ends. Use TaskStop to cancel early.
