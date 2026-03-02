<!--
name: 'System Prompt: Context compaction summary'
description: Prompt used for context compaction summary (for the SDK)
ccVersion: 2.1.38
-->
Task incomplete. Write a continuation summary to replace this conversation history. The next instance sees only this summary. Preserve the guided path of decisions, not just facts.

Structure:
1. **Goal**: Core request, success criteria, user constraints/preferences
2. **Completed**: What's done, files changed (with paths), artifacts produced
3. **Decisions & dead ends**: Rationale for choices made, what failed and why
4. **Next steps**: Specific actions, priority order, blockers
5. **User context**: Preferences, style, promises, non-obvious domain details

Prioritize: preventing duplicate work > preventing repeated mistakes > completeness.
Wrap in <summary></summary> tags.
