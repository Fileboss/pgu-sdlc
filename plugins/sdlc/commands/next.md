---
description: Approve the current phase and start the next one (the sdlc gate)
argument-hint: "[item-slug to start a new item]"
allowed-tools: Bash, Read, Edit, Write, Skill
---

The user approves the current phase. Run from the project root:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sdlc.py" next` — or, when no item is in progress, `... next --item <slug>` with a short kebab-case slug for the item (from the arguments: $ARGUMENTS, or ask). It updates `.sdlc/state.json` and prints the new phase. If it prints `done:`, move the item to "Done" in BACKLOG.md and stop.

When starting a new item, add it under "In progress" in BACKLOG.md, linking `docs/specs/<slug>/` when the spec module is on.

Then run the new phase, following AGENTS.md:

| Phase | Do |
|---|---|
| spec | `sdlc:grilling` (or `sdlc:grill-with-docs` when the decisions module is on), then `sdlc:to-spec` |
| plan | `sdlc:to-tickets` |
| implement | Work the tickets frontier first, or the item itself without the plan module; use `sdlc:tdd` when the tdd module is on. `make lint test` must pass. |
| review | the built-in `code-review` skill on the item's diff |
| commit | propose the commit message(s) following the conventions, commit on approval, mark tickets `done` |

At the end of the phase, stop and summarise for the gate, unless autonomy is on in `.sdlc.yml`: then invoke `sdlc:next` yourself, still asking before pushing to `main`, tagging or changing a data schema.
