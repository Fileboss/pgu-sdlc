# sdlc v1 — design

Settled in a grilling session on 2026-11-12. Goal: make personal AI-assisted projects uniform and reliable, the main pain being projects that each work differently. The workflow is modular: a small project takes only what it needs.

## Shape

- A Claude Code plugin named `sdlc` that also ships a mod (UI), distributed from this repo as a git marketplace.
- Installed once, **enabled per project** (`--scope project`), never globally.
- Versioned with semver (`vX.Y.Z` tags) and the commit convention below. No self-validation: it is used and iterated on.

## Project configuration

- `.sdlc.yml` is the single source of truth: modules (à la carte, no presets, chosen by the user), stack profiles, autonomy, stop check.
- `AGENTS.md` holds a generated block rendered from `.sdlc.yml`; the rest of the file is free. `CLAUDE.md` only imports it (`@AGENTS.md`).
- `.sdlc/state.json` (committed) holds the current BACKLOG item and its phase, updated at phase transitions only.

## Modules

- `core`, always on: AGENTS.md, uniform Makefile (`dev`, `test`, `lint`, `build`), guardrails:
  - no `.env*` access (`.env.example` allowed);
  - push allowed except to `main` and except tags, which need the user's explicit request;
  - no destructive docker commands;
  - stop check `make lint test` (can be disabled).
- Optional: `spec`, `plan`, `decisions`, `tdd`, `review`, `commit`, `release`, `ci`, `docker`, `pr`, `handoff`, `retro`.

## Cycle

- Per BACKLOG item: spec -> plan -> implement -> review -> commit, keeping only active modules. Releases are project-wide.
- Gates between every big phase by default. Autonomy can be switched on in `.sdlc.yml` or for one run in the session; push to `main`, release tags and data schema changes stay gated.
- Programmable gates (mod) block only irreversible or outgoing actions (commit without review when `review` is on, push, tag); otherwise the phase is a reminder.

## Artefacts

Files only: `docs/specs/`, BACKLOG.md, ADR and GLOSSARY in the `grill-with-docs` format. Everything is written in English; the user talks in French.

## Git conventions

- Trunk-based on `main`, light protection (no force-push, no deletion). Branches and PRs (merge commit, no squash) only with the `pr` module.
- Commits: `Scope: imperative description`, optional milestone prefix (`M11.1: ...`).
- Release: the AI proposes the semver bump and the CHANGELOG entry; the user approves.

## Stack profiles

`sveltekit-pnpm`, `python-uv`, `java-spring-maven`, `rust-cargo`, `go`. Several per project for monorepos (`name:subdir`).

## External skills

Matt Pocock's skills only, vendored at a pinned commit and updated with `make sync-pocock` after reading the diff. Selection: grilling, grill-with-docs, to-spec, to-tickets, tdd, implement, pr, handoff, retro, diagnosing-bugs, prototype, codebase-design, setup-matt-pocock-skills, writing-for-agents. Review uses Claude Code's built-in `/code-review`.

## UI (mod)

Collapsed: the current phase. Expanded: module toggles, gates/auto switch, "next phase" button. The panel writes `.sdlc.yml`.

## Delivery order

1. Core and `/sdlc:init`.
2. Pocock skills; spec, plan, tdd and review modules.
3. The mod.
4. Release, CI, docker, remaining profiles.

No migration of existing projects for now.
