---
title: sdlc v1 design
tags: [sdlc, spec]
date: 2026-11-12
status: accepted
---

# sdlc v1 — design

Settled in a grilling session on 2026-11-12. Goal: make personal AI-assisted projects uniform and reliable, the main pain being projects that each work differently. The workflow is modular: a small project takes only what it needs.

## Shape

- A Claude Code plugin named `sdlc` that also ships a mod (UI), distributed from this repo as a git marketplace.
- Installed once, **enabled per project** (`--scope project`), never globally.
- Versioned with semver (`vX.Y.Z` tags) and the commit convention below. No self-validation: it is used and iterated on.

## Project configuration

- `.sdlc.yml` is the single source of truth: modules (à la carte, no presets, chosen by the user), stack profiles, gates, stop check.
- `AGENTS.md` holds a generated block rendered from `.sdlc.yml`; the rest of the file is free. `CLAUDE.md` only imports it (`@AGENTS.md`).
- `.sdlc/state.json` (committed) holds the current BACKLOG item and its phase, updated at phase transitions only.

## Modules

- `core`, always on: AGENTS.md, uniform Makefile (`dev`, `test`, `lint`, `build`), guardrails:
  - no `.env*` access (`.env.example` allowed);
  - push allowed except to `main` and except tags, which need the user's explicit request;
  - no destructive docker commands;
  - stop check `make lint test` (can be disabled);
  - `.github/workflows/security.yml`: Trivy filesystem scan of every lockfile (HIGH/CRITICAL with a fix fails the run) and gitleaks on the history, on push to `main`, on PRs and weekly; not a required check, which would block trunk-based pushes: a failure mails the owner;
  - `.github/dependabot.yml`: weekly PRs for the profile's ecosystem, GitHub Actions and the Docker base image. Actions are pinned by commit SHA (Node 20 runners are gone since 2026-09-16, so stale majors break).
- Optional: `spec`, `plan`, `decisions`, `tdd`, `review`, `commit`, `release`, `ci`, `docker`, `pr`, `handoff`, `retro`.

## Cycle

- Per BACKLOG item: spec -> plan -> implement -> review -> commit, keeping only active modules. Releases are project-wide.
- `/sdlc:next` advances `.sdlc/state.json` and runs the next phase. `gates` in `.sdlc.yml` says where the AI stops for approval: `commit` (default: once per item, before committing), `all` (every phase) or `none`. Push to `main`, release tags and data schema changes always need approval. Lightened before the first real test (2026-11-12): solo dev, one gate is enough.
- `/sdlc:quick <slug>` starts an item that skips spec and plan: straight to implement → review → commit.
- Programmable gates (mod) block only irreversible or outgoing actions (commit without review when `review` is on, push, tag); otherwise the phase is a reminder.

## Artefacts

Files only. BACKLOG.md indexes the items; each item has `docs/specs/<slug>/spec.md` and tickets in `docs/specs/<slug>/issues/NN-*.md` (Pocock's local-markdown tracker, moved from `.scratch/` so it is committed). ADRs in `docs/adr/` and `GLOSSARY.md`, written by `domain-modeling`. `docs/agents/issue-tracker.md` and `domain.md` tell the skills where things live; `/sdlc:init` writes them, replacing `setup-matt-pocock-skills`. Everything is written in English; the user talks in French.

Human docs (`docs/**`, BACKLOG, CHANGELOG, GLOSSARY, README; not AGENTS/CLAUDE) are written for Obsidian: YAML frontmatter (`title`, `tags`, `date`, `status`; none on README, which GitHub would show as a table), relative markdown links rather than wikilinks so they also work on GitHub and for agents, callouts and mermaid. `/sdlc:init` can symlink them into `~/Documents/obsidian/perso/<project>/`: one copy, always current.

## Git conventions

- Trunk-based on `main`, light protection (no force-push, no deletion). Branches and PRs (merge commit, no squash) only with the `pr` module.
- Commits: `Scope: imperative description`, optional milestone prefix (`M11.1: ...`).
- Release: the AI proposes the semver bump and the CHANGELOG entry; the user approves.

## Stack profiles

`sveltekit-pnpm`, `node-ts-pnpm`, `python-uv`, `java-spring-maven`, `rust-cargo`, `go`. Several per project for monorepos (`name:subdir`).

Every runtime starts on the most recent LTS (most recent stable where none exists), looked up online at init (`sdlc.py lts`: nodejs.org, Adoptium, endoflife.date, go.dev) and pinned to its major or minor in the file CI reads: `.nvmrc`, `.python-version`, `.java-version`, `go.mod`. Rust follows stable. The same rule applies to frameworks, tools and Docker base images, written in AGENTS.md.

TypeScript profiles share one ESLint and Prettier config, copied at init (marked `sdlc eslint v1`): `js` + `typescript-eslint` recommended + prettier, `no-undef` off; the svelte profile adds `eslint-plugin-svelte` and `svelte/button-has-type`. Prettier: tabs, single quotes, no trailing comma, width 100. No type-checked rules (slow on small projects). Angular stays out until a project needs it.

## External skills

Matt Pocock's skills only, vendored at a pinned commit and updated with `make sync-pocock` after reading the diff. Selection: grilling, grill-with-docs, domain-modeling (called by grill-with-docs), to-spec, to-tickets, tdd, pr, handoff, retro, diagnosing-bugs, prototype, codebase-design, writing-for-agents. Not vendored: `implement` (it chains implement, review and commit without gates; `/sdlc:next` drives those phases instead) and `setup-matt-pocock-skills` (replaced by `/sdlc:init`). Review uses Claude Code's built-in `code-review`. The sync rewrites skill-to-skill calls to the `sdlc:` namespace and makes to-spec, to-tickets and grill-with-docs model-invocable so phases can chain.

## UI (mod)

Collapsed: the current phase. Expanded: module toggles, gates switch, "next phase" button. The panel writes `.sdlc.yml`.

## Delivery order

1. Core and `/sdlc:init`.
2. Pocock skills; spec, plan, tdd and review modules.
3. The mod.
4. Release, CI, docker, remaining profiles.

No migration of existing projects for now.
