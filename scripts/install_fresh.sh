#!/usr/bin/env bash
set -euo pipefail

# Purpose: clear stale backups/state, reinstall Claude Code, then run apply_and_test.

VERSION="${1:-2.1.63}"

rm -f ~/.tweakcc/cli.js.backup ~/.tweakcc/native-binary.backup ~/.tweakcc/native-binary.pre-reinstall.backup
rm -rf out

npm install -g "@anthropic-ai/claude-code@${VERSION}"

bash scripts/apply_and_test.sh
