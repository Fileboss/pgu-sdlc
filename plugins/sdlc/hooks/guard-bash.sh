#!/bin/sh
# PreToolUse hook (Bash): sdlc core guardrails. Inert outside sdlc projects.
#   1. no command may name a .env file (.env.example stays readable);
#   2. destructive docker commands are refused;
#   3. pushing to main, or pushing tags, asks the user first.
# String matching catches mistakes, not a determined bypass.
# Exit 2 blocks the call and shows stderr to the agent.
input=$(cat)
root=${CLAUDE_PROJECT_DIR:-$(printf '%s' "$input" | jq -r '.cwd // "."')}
[ -f "$root/.sdlc.yml" ] || exit 0
command=$(printf '%s' "$input" | jq -r '.tool_input.command // empty')

block() {
  echo "Blocked by sdlc: $1" >&2
  exit 2
}

ask() {
  jq -n --arg reason "sdlc: $1" \
    '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "ask", permissionDecisionReason: $reason}}'
  exit 0
}

if ! printf '%s' "$command" | perl -ne 'exit 1 if /\.env(?!\.example\b)(?![\w-])/'; then
  block "this project forbids reading or touching .env files (secrets). Use .env.example."
fi

if printf '%s' "$command" | grep -Eq \
  'docker(-| )compose[^;&|]* down[^;&|]*(-v\b|--volumes)|docker volume (rm|prune)|docker system prune'; then
  block "destructive docker command (volumes or system prune). Ask the user to run it."
fi

# Prints "tag" or "main" for the first sensitive git push; a push without
# refspec targets the current branch.
target=$(printf '%s' "$command" | BRANCH=$(git -C "$root" branch --show-current 2>/dev/null) perl -ne '
  while (/\bgit\s+push\b([^;&|]*)/g) {
    my @args = split " ", $1;
    if (grep { $_ eq "--tags" || $_ eq "--follow-tags" } @args) { print "tag"; exit }
    my @refs = grep { !/^-/ } @args;
    shift @refs;
    @refs = ($ENV{BRANCH}) unless @refs;
    for (@refs) {
      if (m{refs/tags/|^v\d}) { print "tag"; exit }
      if (m{(^|:|/)main$}) { print "main"; exit }
    }
  }')
case "$target" in
  main) ask "pushing to main needs the user's explicit request." ;;
  tag) ask "pushing a release tag needs the user's explicit request." ;;
esac
exit 0
