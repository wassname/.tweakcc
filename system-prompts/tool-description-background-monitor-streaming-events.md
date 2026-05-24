<!--
name: 'Tool Description: Background monitor (streaming events)'
description: >-
  Describes the background monitor tool that streams stdout events from
  long-running scripts as chat notifications, with guidelines on script quality,
  output volume, and selective filtering
ccVersion: 2.1.119
-->

Start a background monitor that streams events from a long-running script. Each stdout line becomes a notification. Exit ends the watch.

Pick by notification count:
- One: use Bash with run_in_background and a command that exits on condition
- Streaming: Monitor with an unbounded command (tail -f, inotifywait -m, polling loop)
