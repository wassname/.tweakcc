<!--
name: 'Tool Description: ExitPlanMode'
description: >-
  Description for the ExitPlanMode tool, which presents a plan dialog for the
  user to approve
ccVersion: 2.1.14
-->
Signal that your plan is written and ready for user review.

- Plan must already be written to the plan file from the plan mode system message.
- This tool reads from that file -- does NOT take plan content as parameter.
- Only for implementation plans (code tasks). NOT for research/exploration.
- If unresolved questions remain, use AskUserQuestion first.
- Do NOT use AskUserQuestion to ask "Is this plan okay?" -- that's what this tool does.
