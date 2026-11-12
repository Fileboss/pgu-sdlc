#!/bin/sh
# PreToolUse hook (Read|Edit|Write|MultiEdit): no file tool may open a .env file.
# .env.example is the committed template and stays allowed. Inert outside sdlc projects.
input=$(cat)
root=${CLAUDE_PROJECT_DIR:-$(printf '%s' "$input" | jq -r '.cwd // "."')}
[ -f "$root/.sdlc.yml" ] || exit 0
path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')
case "$(basename "${path:-x}")" in
  .env.example) exit 0 ;;
  .env | .env.*)
    echo "Blocked by sdlc: $path holds secrets. Use .env.example." >&2
    exit 2
    ;;
esac
exit 0
