<!--
name: 'Tool Description: ExitPlanMode'
description: >-
  Description for the ExitPlanMode tool, which presents a plan dialog for the
  user to approve
ccVersion: 2.1.14
variables:
  - ASK_USER_QUESTION_TOOL_NAME
-->

Signal that your plan is written to the plan file and ready for user review. Only use after writing an implementation plan (not for research/exploration). Do not use AskUserQuestion to ask "is this plan okay?" -- that's what this tool does. Resolve questions with AskUserQuestion before calling this.
