## Workflow (sdlc)

Stack profiles: {profiles}. Active modules: {modules}.

Each BACKLOG.md item goes through these phases: {phases}. Releases are project-wide, not per item.

- `.sdlc/state.json` holds the current item and phase. Change it only through `sdlc:next` (a phase transition; at a gate, the user runs it); commit it with the work. `/sdlc:quick <slug>` starts an item that skips spec and plan.
- On a new session, read `.sdlc/state.json` and BACKLOG.md first, then resume where they say.

{gates}

## Commands

Use the Makefile entry points, never the underlying tools directly: `make dev`, `make test`, `make lint`, `make build`.
Run `make lint test` before declaring work done.

## Conventions

- Write everything in English: code, comments, commits, docs, BACKLOG.md. The user may write in French; answer in French.
- Commit messages: `Scope: imperative description`, the scope a capitalised word (`Auth: add SameSite cookie`, `Backlog: mark M11 done`). Prefix a milestone id when there is one (`M11.1: ...`). One logical change per commit.
- Git: trunk-based on `main` unless the `pr` module is active. Pushing to `main` needs the user's explicit request; other branches may be pushed.
- Never read or write `.env` files; `.env.example` is the committed template.

## Docs for humans (read in Obsidian)

Human docs are `docs/**`, BACKLOG.md, CHANGELOG.md, GLOSSARY.md and README.md (not AGENTS.md or CLAUDE.md). The user reads them in Obsidian, so:

- Start each with YAML frontmatter: `title`, `tags` (a list), `date` (YYYY-MM-DD, creation), and `status` where it means something (`draft`, `accepted`, `done`). README.md has none: GitHub would show it as a table.
- Link with relative markdown links (`[ADR 0001](../adr/0001-x.md)`), never `[[wikilinks]]`, so links work in Obsidian, on GitHub and for agents.
- Use Obsidian callouts (`> [!note]`, `> [!warning]`) for asides and mermaid for diagrams.
