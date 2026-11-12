## Workflow (sdlc)

Stack profiles: {profiles}. Active modules: {modules}.

Each BACKLOG.md item goes through these phases: {phases}. Releases are project-wide, not per item.

- `.sdlc/state.json` holds the current item and phase. Change it only through `/sdlc:next`, which is the gate approval; commit it with the work.
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
