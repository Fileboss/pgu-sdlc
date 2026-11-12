---
description: Start a small item that skips spec and plan - straight to implementation
argument-hint: "<item-slug> [what to do]"
allowed-tools: Bash, Read, Edit, Write, Skill
---

Start a quick item: a fix or a small change that needs no spec. From the project root:

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sdlc.py" next --quick --item <slug>` — the slug is the first word of the arguments ($ARGUMENTS), kebab-case; the rest describes the work. If an item is already in progress the script refuses: finish or discuss it first.

Add the item under "In progress" in BACKLOG.md, then run the implement phase as `/sdlc:next` describes it (tdd when the module is on, `make lint test` green). The item then goes through review and commit like any other, with the gates `.sdlc.yml` sets.
