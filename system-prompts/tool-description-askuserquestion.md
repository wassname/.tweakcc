<!--
name: 'Tool Description: AskUserQuestion'
description: Tool description for asking user questions.
ccVersion: 2.1.47
variables:
  - EXIT_PLAN_MODE_TOOL_NAME
-->
Ask user questions during execution: gather preferences, clarify ambiguity, get decisions on implementation choices.

- Users can always select "Other" for custom input
- multiSelect: true for non-exclusive choices
- Recommended option: first in list with "(Recommended)" suffix
- Plan mode: clarify before finalizing. Do NOT ask "Is my plan ready?" -- use ExitPlanMode.
- IMPORTANT: Do not reference "the plan" in questions (e.g. "Does the plan look good?") because the user cannot see the plan until you call ${EXIT_PLAN_MODE_TOOL_NAME}. Use ExitPlanMode for plan approval.
