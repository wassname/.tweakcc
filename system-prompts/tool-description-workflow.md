<!--
name: 'Tool Description: Workflow'
description: >-
  Describes the Workflow tool for running deterministic multi-subagent
  orchestration scripts, including opt-in requirements, script metadata, agent
  hooks, concurrency, budgeting, quality patterns, and resume behavior
ccVersion: 2.1.146
variables:
  - WORKFLOW_TOOL_NAME
  - WORKFLOW_SCRIPT_PATH_NOTE
  - WORKFLOW_AGENT_ISOLATION_OPTION
  - WORKFLOW_AGENT_ISOLATION_NOTE
  - WORKFLOW_GROUP_PREFIX
-->

Execute a workflow script that orchestrates multiple subagents deterministically. Returns a task ID; a \<task-notification\> arrives on completion.

ONLY call when the user has explicitly opted in: "ultrawork" keyword, direct request for workflow/multi-agent orchestration, a skill/command that says to, or a named/saved workflow. For anything else, use the Agent tool or describe what a workflow could do and ask.

Script format: \`export const meta = {name, description, phases: [{title, detail}]}\` followed by async body using: agent(prompt, opts?), pipeline(items, ...stages), parallel(thunks), phase(title), log(msg), budget.remaining(). Default to pipeline(). Use parallel() only when stage N genuinely needs all of stage N-1's results (dedup, early-exit on zero). Subagents return raw data (not human-facing text). Use schema option for structured output with auto-validation.

Concurrency: min(16, cores-2) simultaneous agents, max 1000 total. No Date.now()/Math.random()/new Date() (breaks resume). No fs/Node globals. Resume via resumeFromRunId (longest unchanged prefix is cached).
