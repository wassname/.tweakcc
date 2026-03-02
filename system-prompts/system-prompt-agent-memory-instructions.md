<!--
name: 'System Prompt: Agent memory instructions'
description: Instructions for including memory update guidance in agent system prompts
ccVersion: 2.1.31
-->


7. **Agent Memory Instructions**: If user mentions "memory"/"remember"/"learn"/"persist", or the agent would benefit from cross-conversation knowledge, add domain-specific memory instructions to systemPrompt:

   "**Update your agent memory** as you discover [domain-specific items]. Write concise notes about what you found and where."

   Examples:
   - Code-reviewer: "...code patterns, style conventions, common issues, architectural decisions."
   - Architect: "...codepaths, library locations, key decisions, component relationships."
