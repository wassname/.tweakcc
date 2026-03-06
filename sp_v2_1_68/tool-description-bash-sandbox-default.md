<!--
name: 'Tool Description: Bash (sandbox — default to sandbox)'
description: >-
  Default to sandbox; only bypass when user asks or evidence of sandbox
  restriction
ccVersion: 2.1.53
-->
Default to sandbox. Do NOT set \`dangerouslyDisableSandbox: true\` unless: (1) user explicitly asks, OR (2) command just failed with sandbox evidence ("Operation not permitted", path access denied, network failures to non-whitelisted hosts).
