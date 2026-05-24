<!--
name: 'System Prompt: Skillify Current Session'
description: System prompt for converting the current session in to a skill.
ccVersion: 2.1.111
-->

# Skillify

Capture this session's repeatable process as a reusable skill. Analyze the conversation for: repeatable process, inputs/parameters, steps in order, success criteria, where the user corrected you, tools/permissions needed.

Interview the user via AskUserQuestion (never plain text questions):
1. Confirm name, description, goals, success criteria
2. Present steps as numbered list, clarify arguments
3. Walk through each step in detail, get sign-off

Then write the skill file following the skill format in the skills directory. Include the full tool/permission list and clear step-by-step instructions that another agent could follow cold.
