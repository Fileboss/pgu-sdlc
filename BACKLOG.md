---
title: Backlog
tags: [backlog, sdlc]
---

# Backlog

## In progress

## To do

- Watch typescript-eslint for TypeScript 7 support, then drop the `typescript@^6` pin in the profiles.
- Try the whole cycle on a real new project and trim whatever slows it down.
- Decide what to do with the 10 skill copies in ~/.claude/skills (the plugin is per project, so deleting them removes them from other projects).

## Done

- v0.6.0 — Human docs written for Obsidian (frontmatter, relative markdown links, callouts, mermaid) and linked into the central vault by symlinks; shared ESLint/Prettier config for every TypeScript profile (sdlc eslint v1), new `node-ts-pnpm` profile.
- v0.5.0 — Lighter process: `gates: commit|all|none` (default one stop before commit, replaces autonomy), `/sdlc:quick` items that skip spec and plan, spec and plan asked to stay proportionate.
- v0.4.0 — Step 4: `/sdlc:release` (one approval: bump, CHANGELOG, version files, commit, tag), ci module (GitHub Actions per profile calling `make lint test`), docker module (ghcr image on tag), monorepo `make dev` in parallel.
- v0.3.1 — Band shows the plan's 5-hour and weekly usage with reset times.
- v0.3.0 — Step 3: the mod — band above the prompt (item, phase, gates/auto), expandable panel (module toggles, autonomy, approve next), commit gate when review is on; `sdlc.py set` and `status --json`.

- v0.2.0 — Step 2: Pocock skills vendored at a pinned commit (`make sync-pocock`), spec/plan/decisions/tdd/review wired to them, local-markdown tracker under `docs/specs/`, `/sdlc:next` phase gate, stop check limited to code changes outside spec/plan.

- v0.1.0 — Step 1: marketplace, plugin skeleton, `.sdlc.yml`, core guardrails, stack profiles, `/sdlc:init`, `/sdlc:status`, `/sdlc:sync`.
