---
description: Show the sdlc configuration and the current item and phase
allowed-tools: Bash
---

Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sdlc.py" status` from the project root and show its output as is. If it fails because `.sdlc.yml` is missing, suggest `/sdlc:init`.
