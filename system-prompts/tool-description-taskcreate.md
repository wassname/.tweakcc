<!--
name: 'Tool Description: TaskCreate'
description: Tool description for TaskCreate tool
ccVersion: 2.1.19
variables:
  - CONDTIONAL_TEAMMATES_NOTE
  - CONDITIONAL_TASK_NOTES
-->
Create a structured task list for multi-step coding sessions. Shows user progress.

## When to Use
- 3+ step tasks, plan mode, user provides multiple tasks${CONDTIONAL_TEAMMATES_NOTE}
- Mark in_progress BEFORE starting, completed IMMEDIATELY after

## When NOT to Use
- Single trivial task (<3 steps), purely conversational

## Fields
- **subject**: imperative ("Fix auth bug")
- **description**: detailed, with context and acceptance criteria
- **activeForm**: present continuous ("Fixing auth bug") -- shown in spinner. ALWAYS provide.

${CONDITIONAL_TASK_NOTES}Check TaskList first to avoid duplicates. Use TaskUpdate for dependencies (blocks/blockedBy).
