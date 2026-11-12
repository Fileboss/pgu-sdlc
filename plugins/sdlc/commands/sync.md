---
description: Regenerate AGENTS.md and derived files after editing .sdlc.yml
allowed-tools: Bash, Read
---

`.sdlc.yml` was edited. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sdlc.py" render` from the project root, then show the diff of `AGENTS.md` (`git diff AGENTS.md`) and summarise what changed in the workflow. An existing Makefile is never overwritten: if a profile was added, propose the matching targets and edit the Makefile only on approval. For each `differs from sdlc:` line, offer to replace the project's file with sdlc's, as `/sdlc:init` does.
