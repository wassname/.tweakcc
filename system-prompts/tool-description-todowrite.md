<!--
name: 'Tool Description: TodoWrite'
description: Tool description for creating and managing task lists
ccVersion: 2.1.84
variables:
  - EDIT_TOOL_NAME
-->

Create and manage a structured task list for the current session. Helps track progress and show the user what's happening. Follow CLAUDE.md task conventions if present.

## When to use
- Multi-step tasks (3+ steps), user-provided task lists, plan mode
- After receiving new instructions: capture requirements as todos immediately
- Skip for single trivial tasks

## Task states
- pending: not started
- in_progress: currently working; exactly ONE task must have this state
- completed: finished successfully. Only mark completed when FULLY done -- not if tests fail, implementation is partial, or errors unresolved.

## Management
- Mark in_progress BEFORE starting work, completed IMMEDIATELY after finishing
- Complete the current task before starting another. If blocked, keep it in_progress and add the task needed to unblock it.
- Break complex tasks into specific, actionable items
- Remove tasks no longer relevant
- Provide both content ("Fix auth bug") and activeForm ("Fixing auth bug")
