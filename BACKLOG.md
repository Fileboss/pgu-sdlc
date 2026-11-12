# Backlog

## In progress

## To do

- Step 2: vendor Matt Pocock's skills (pinned commit, `make sync-pocock`) and wire spec, plan, tdd and review.
  - [ ] Vendor: grilling, grill-with-docs, to-spec, to-tickets, tdd, implement, pr, handoff, retro, diagnosing-bugs, prototype, codebase-design, setup-matt-pocock-skills, writing-for-agents.
  - [ ] Check whether to-spec / to-tickets can write to local markdown (docs/specs, BACKLOG.md); otherwise write thin in-house skills.
  - [ ] Align the decisions module's ADR path and format with grill-with-docs.
  - [ ] `/sdlc:next`: phase transition that updates .sdlc/state.json (the gate approval).
  - [ ] Remove the 10 copied skills from ~/.claude/skills.
- Step 3: the mod — collapsed band with the current phase; expanded panel with module toggles, gates/auto switch, "next phase"; programmable gates (commit without review when review is on).
- Step 4: `/sdlc:release` (semver, CHANGELOG), ci and docker module scaffolding, remaining profiles.
- Makefile `dev` with several profiles runs them one after another; consider `make -j`.

## Done

- v0.1.0 — Step 1: marketplace, plugin skeleton, `.sdlc.yml`, core guardrails, stack profiles, `/sdlc:init`, `/sdlc:status`, `/sdlc:sync`.
