---
description: Cut a release - semver bump, CHANGELOG entry, version files, commit and tag (one approval)
argument-hint: "[major|minor|patch|X.Y.Z]"
allowed-tools: Bash, Read, Edit, Write
---

Prepare a release in one pass, then ask for a single approval.

1. Find the last tag: `git describe --tags --abbrev=0` (none: this is the first release, propose `v0.1.0`). Refuse if the working tree is dirty.
2. Read the commits since it: `git log <tag>..HEAD --oneline`. Pick the bump yourself unless the arguments fix it ($ARGUMENTS): major for a breaking change, minor for anything new, patch for fixes only. Pre-1.0, a breaking change is a minor.
3. Prepend the entry to `CHANGELOG.md` (create it if missing, with frontmatter `title: Changelog` and `tags: [changelog]`, then a `# Changelog` title): `## vX.Y.Z — YYYY-MM-DD`, then short user-facing bullets grouped under `### Added`, `### Changed`, `### Fixed` (omit empty groups; skip pure chores).
4. Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/sdlc.py" bump X.Y.Z` to update package.json, pyproject.toml or Cargo.toml. For other stacks (Maven, Go), say what holds the version, if anything.
5. Show the version, the reason for the bump and the CHANGELOG entry, and ask once: "Release vX.Y.Z?" On yes: `git commit -am "Release: vX.Y.Z"` (adding CHANGELOG.md if new), then `git tag vX.Y.Z`. Do not push: tell the user `git push --follow-tags` publishes it (and builds the image when the docker module is on).
