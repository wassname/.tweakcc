<!--
name: 'Tool Description: Workflow'
description: >-
  Describes the Workflow tool for running deterministic multi-subagent
  orchestration scripts, including opt-in requirements, script metadata, agent
  hooks, concurrency, budgeting, quality patterns, and resume behavior
ccVersion: 2.1.217
variables:
  - AGENT_TOOL_NAME
  - WORKFLOW_INVOCATION_QUALIFIER
  - WORKFLOW_SCRIPT_PATH_NOTE
  - WORKFLOW_AGENT_ISOLATION_OPTION
  - WORKFLOW_AGENT_ISOLATION_NOTE
  - WORKFLOW_GROUP_PREFIX
-->
Execute a workflow script that orchestrates multiple subagents deterministically. Runs in the background: returns a task ID immediately, a \<task-notification\> arrives on completion. Use /workflows to watch progress.

ONLY call when the user has explicitly opted into multi-agent orchestration: the "ultracode" keyword, a direct request for a workflow / multi-agent orchestration, a skill or command that says to, or a named/saved workflow. Workflows can spawn dozens of agents and burn many tokens, so the user must ask for that scale, not have it inferred. For anything else, use the Agent tool or briefly describe what a workflow could do and ask.

Script format: \`export const meta = {name, description, phases: [{title, detail}]}\` (pure literal) followed by an async body using: agent(prompt, opts?), pipeline(items, ...stages), parallel(thunks), phase(title), log(msg), workflow(nameOrRef, args?), and the budget/args globals. Default to pipeline(); reach for parallel() only when stage N genuinely needs all of stage N-1's results (dedup, early-exit on zero). Subagents return raw data, not human-facing text; pass a JSON schema via the schema option for validated structured output.

Concurrency: min(16, cores-2) simultaneous agents, 1000 total cap, 4096 items per parallel/pipeline call. Plain JS, not TypeScript. No Date.now()/Math.random()/new Date() (breaks resume); no fs/Node globals. Resume via resumeFromRunId (longest unchanged agent() prefix is cached). Quality patterns to compose: adversarial verify (N skeptics per finding), perspective-diverse verify, judge panel, loop-until-dry, multi-modal sweep, completeness critic; log anything silently dropped.
