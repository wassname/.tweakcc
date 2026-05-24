<!--
name: 'Tool Description: TeammateTool'
description: Tool for managing teams and coordinating teammates in a swarm
ccVersion: 2.1.88
-->

Create a team to coordinate multiple agents. Use when the user explicitly asks for a team/swarm or a task clearly benefits from parallel agent work. Creates a team config and corresponding task list. Workflow: TeamCreate -> create tasks -> assign to teammates via Agent tool -> coordinate via SendMessage. Match agent types to task needs (read-only agents can't edit files).
