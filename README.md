# pgu-sdlc

A modular AI SDLC for personal projects, shipped as a Claude Code plugin (`sdlc`) from this marketplace repo.

Each project picks its modules à la carte in `.sdlc.yml`; the plugin renders `AGENTS.md`, a uniform `Makefile` and guardrails from it. See [docs/specs/sdlc-v1.md](docs/specs/sdlc-v1.md) for the design.

## Install

```sh
claude plugin marketplace add Fileboss/pgu-sdlc   # once (or a local path while developing)
```

The plugin is enabled per project, never globally. In a project:

```sh
claude plugin install sdlc@pgu-sdlc --scope project   # writes .claude/settings.json
```

Then run `/sdlc:init` in Claude Code.

## Commands

| Command | Effect |
|---|---|
| `/sdlc:init` | Choose stack profiles, modules and autonomy; generate `.sdlc.yml`, `AGENTS.md`, `CLAUDE.md`, `Makefile`, `BACKLOG.md`; optionally protect `main` |
| `/sdlc:status` | Show configuration, phases and the current item |
| `/sdlc:sync` | Regenerate `AGENTS.md` after editing `.sdlc.yml` |
| `/sdlc:release [bump]` | Propose the semver bump and CHANGELOG entry, bump version files, then commit and tag on one approval (no push) |
| `/sdlc:next [item]` | Gate approval: start an item or move it to its next phase, then run that phase |

Vendored skills (Matt Pocock, MIT) are namespaced `sdlc:*`; see [plugins/sdlc/skills/VENDORED.md](plugins/sdlc/skills/VENDORED.md). `/sdlc:handoff` and `/sdlc:retro` are user-invoked.

## Band and panel (mod)

In an sdlc project a one-line band sits above the prompt: `▸ sdlc · <item> · <phase> · gates|auto · 5h 23% ↻14:00 · week 41% ↻Mon`: the plan's 5-hour and weekly usage, in yellow past 80% and red past 95% (shown on a subscription only). Press `▸` to expand it: module toggles, a gates/auto switch and "Approve <phase> → next". Each press goes through `scripts/sdlc.py set|next`, so `.sdlc.yml` stays the source of truth and `AGENTS.md` is re-rendered.

With the review module on, the mod denies `git commit` while an item is in progress and not yet in its review or commit phase.

## Layout

```
.claude-plugin/marketplace.json
plugins/sdlc/
  commands/         slash commands
  hooks/            guardrails (.env, destructive docker, push to main/tags), the stop check,
                    and register.tsx: the mod (band, panel, commit gate)
  tests/            the mod's tests (make test)
  types/            the mod's state contract
  profiles/         stack profiles: Makefile commands per stack
  scripts/sdlc.py   reads .sdlc.yml, renders derived files, moves phases (stdlib only)
  skills/           vendored skills, never edited by hand
  templates/        AGENTS.md block, one snippet per module
```

## Develop

```sh
claude --plugin-dir plugins/sdlc   # load the working copy in a session
make validate
make test
make sync-pocock [REF=<sha>]       # re-vendor the skills, then review the diff
```
