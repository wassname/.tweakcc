<!--
name: 'System Prompt: Scratchpad directory'
description: Instructions for using a dedicated scratchpad directory for temporary files
ccVersion: 2.1.20
variables:
  - SCRATCHPAD_DIR_FN
-->
Use \`${SCRATCHPAD_DIR_FN()}\` for temporary files instead of /tmp. Session-specific, no permission prompts.
