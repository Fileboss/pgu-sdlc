# Domain docs

How skills consume this repo's domain documentation. Layout adapted from github.com/mattpocock/skills (MIT).

## Before exploring, read these

- `GLOSSARY.md` at the repo root.
- `docs/adr/`: the ADRs touching the area you are about to work in.

If they do not exist, proceed silently. `sdlc:domain-modeling` (reached through `sdlc:grill-with-docs`) creates them when terms or decisions get resolved.

## Use the glossary's vocabulary

When your output names a domain concept (ticket title, test name, refactor proposal), use the term as `GLOSSARY.md` defines it.

## Flag ADR conflicts

If your output contradicts an ADR, say so explicitly instead of silently overriding it: _Contradicts ADR-0007 (...), but worth reopening because..._
