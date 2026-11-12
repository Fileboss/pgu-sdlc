# Issue tracker: local markdown

Specs and tickets for this repo live as committed markdown files under `docs/specs/`. BACKLOG.md is the index of items; each item in progress links to its folder.

## Conventions

- One item per directory: `docs/specs/<item-slug>/`, the slug being the `item` of `.sdlc/state.json`.
- The spec is `docs/specs/<item-slug>/spec.md`.
- Tickets are one file each at `docs/specs/<item-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order, never a single combined file.
- Each file starts with YAML frontmatter (`title`, `tags`, `date`, `status`), as AGENTS.md says for human docs. Triage state is the frontmatter `status`: `ready-for-agent`, `in-progress` or `done`. A ticket's blockers go in `blocked_by` (a list of ticket numbers).
- Comments append to the bottom of the file under a `## Comments` heading.

## When a skill says "publish to the issue tracker"

Create the file under `docs/specs/<item-slug>/` (creating the directory if needed), and make sure the BACKLOG.md item links to that directory.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the ticket number directly.
