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

## Layout

```
.claude-plugin/marketplace.json
plugins/sdlc/
  commands/         slash commands
  hooks/            guardrails (.env, destructive docker, push to main/tags) and the stop check
  profiles/         stack profiles: Makefile commands per stack
  scripts/sdlc.py   reads .sdlc.yml, renders derived files (stdlib only)
  templates/        AGENTS.md block, one snippet per module
```

## Develop

```sh
claude --plugin-dir plugins/sdlc   # load the working copy in a session
claude plugin validate plugins/sdlc
```
