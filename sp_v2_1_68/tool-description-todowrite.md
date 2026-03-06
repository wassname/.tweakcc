<!--
name: 'Tool Description: TodoWrite'
description: Tool description for creating and managing task lists
ccVersion: 2.1.63
variables:
  - EDIT_TOOL_NAME
-->
Create and manage a structured task list for multi-step tasks. Helps track progress and show the user what's happening.

## When to Use
- Complex multi-step tasks (3+ distinct steps)
- Non-trivial tasks requiring planning or multiple operations
- User provides multiple tasks (numbered or comma-separated)
- After receiving new instructions, capture as todos
- When in doubt, use this tool

## When NOT to Use
- Single straightforward task (fewer than 3 trivial steps)
- Purely conversational or informational

## Task States and Management
- States: pending -> in_progress -> completed
- Mark in_progress BEFORE starting; mark completed IMMEDIATELY after finishing
- ONE in_progress at a time
- ONLY mark completed when FULLY accomplished; keep in_progress if blocked/errored
- Remove tasks that are no longer relevant
- Break complex tasks into smaller, actionable steps

Task descriptions must have two forms:
- content: imperative form ("Run tests", "Fix auth bug")
- activeForm: present continuous form shown during execution ("Running tests", "Fixing auth bug")
