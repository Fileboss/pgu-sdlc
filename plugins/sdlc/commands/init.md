---
description: Set up the sdlc workflow in this project (.sdlc.yml, AGENTS.md, Makefile, guardrails)
argument-hint: "[profiles] [modules]"
allowed-tools: Bash, Read, AskUserQuestion
---

Set up the sdlc workflow in the current project. The user decides everything; propose, never pick silently.

1. If `.sdlc.yml` already exists, stop and point to `/sdlc:status` and `/sdlc:sync`.
2. If this is not a git repository, run `git init -b main`.
3. Look at the repo (lockfiles, build files) and propose stack profiles. Available profiles are the file names in `${CLAUDE_PLUGIN_ROOT}/profiles/`. A monorepo takes one `name:subdir` per part (`python-uv:apps/api`). Ask the user to confirm with AskUserQuestion. Arguments, if given: $ARGUMENTS
4. Ask which optional modules to enable (multi-select): spec, plan, decisions, tdd, review, commit, release, ci, docker, pr, handoff, retro. Nothing is preselected; describe each in a few words.
5. Ask whether autonomy is on (default: off, gates at every phase).
6. Run from the project root:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sdlc.py" init --profiles <p1,p2> --modules <m1,m2> [--autonomy]`
   It writes `.sdlc.yml`, the generated block of `AGENTS.md`, `CLAUDE.md` (`@AGENTS.md`), the `Makefile` if absent, `BACKLOG.md`, `.sdlc/state.json` and `.gitignore` entries.
7. If the repo has a GitHub remote, offer to protect `main` (no force-push, no deletion): `sh "${CLAUDE_PLUGIN_ROOT}/scripts/protect-main.sh"`. Run it only on approval. If gh is missing or the API refuses (private repo on a free plan), report it and move on.
8. Show `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sdlc.py" status`, list the files created, and remind the user that nothing is committed yet.
