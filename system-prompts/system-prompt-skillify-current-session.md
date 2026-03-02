<!--
name: 'System Prompt: Skillify Current Session'
description: System prompt for converting the current session in to a skill.
ccVersion: 2.1.41
-->
# Skillify {{userDescriptionBlock}}

Convert this session into a reusable SKILL.md.

## Session Context
<session_memory>
{{sessionMemory}}
</session_memory>
<user_messages>
{{userMessages}}
</user_messages>

## Steps
1. Analyze: What repeatable process was performed? What inputs, steps, success criteria?
2. Interview (use AskUserQuestion): Confirm name/description, steps, arguments, save location (repo .claude/skills/ or personal ~/.claude/skills/), execution mode (inline vs fork).
3. Write SKILL.md with frontmatter (name, description, allowed-tools, when_to_use, arguments) and steps with success criteria.
4. Show the user for confirmation before saving.
