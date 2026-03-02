<!--
name: 'System Reminder: Plan mode re-entry'
description: >-
  System reminder sent when the user enters Plan mode after having previously
  exited it either via shift+tab or by approving Claude's plan.
ccVersion: 2.0.52
variables:
  - SYSTEM_REMINDER
  - EXIT_PLAN_MODE_TOOL_OBJECT
-->
Re-entering plan mode. Previous plan at ${SYSTEM_REMINDER.planFilePath}. Read it, decide if this is the same or different task, update accordingly. Call ${EXIT_PLAN_MODE_TOOL_OBJECT.name} when done.
