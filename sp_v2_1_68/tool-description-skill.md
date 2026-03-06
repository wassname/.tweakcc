<!--
name: 'Tool Description: Skill'
description: Tool description for executing skills in the main conversation
ccVersion: 2.1.23
variables:
  - SKILL_TAG_NAME
-->
Execute a skill. "/<something>" (e.g. /commit) = skill invocation.

- Invoke: \`skill: "name"\` or \`skill: "name", args: "..."\` or \`skill: "namespace:name"\`
- Available skills listed in system-reminder messages
- BLOCKING: invoke Skill tool BEFORE generating response about the task
- NEVER mention a skill without calling this tool
- If <${SKILL_TAG_NAME}> tag already in this turn, skill is loaded -- follow its instructions directly
- Not for built-in CLI commands (/help, /clear)
