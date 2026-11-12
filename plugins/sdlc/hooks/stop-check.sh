#!/bin/sh
# Stop hook: the agent may not finish on a red tree (`make lint test`).
# Exit 2 sends the failure back to the agent instead of ending the turn.
# `stop_hook_active` is set when the agent is already continuing because of
# this hook; letting that stop through avoids an endless fix-and-retry loop.
# Disabled with `stop_check: false` in .sdlc.yml (slow builds).
input=$(cat)
root=${CLAUDE_PROJECT_DIR:-$(printf '%s' "$input" | jq -r '.cwd // "."')}
[ -f "$root/.sdlc.yml" ] && [ -f "$root/Makefile" ] || exit 0
if [ "$(printf '%s' "$input" | jq -r '.stop_hook_active // false')" = "true" ]; then
  exit 0
fi
cd "$root" || exit 0
[ "$(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sdlc.py" get stop_check)" = "true" ] || exit 0
# Nothing changed since the last commit: nothing to check.
[ -n "$(git status --porcelain 2>/dev/null)" ] || exit 0
if ! out=$(make lint test 2>&1); then
  printf 'make lint test failed. Fix it before stopping:\n%s\n' "$(printf '%s' "$out" | tail -25)" >&2
  exit 2
fi
exit 0
