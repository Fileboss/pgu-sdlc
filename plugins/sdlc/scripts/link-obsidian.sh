#!/bin/sh
# Show this project's human docs in the central Obsidian vault, without copying:
# <vault>/<project>/ holds symlinks to docs/ and the root docs of the repo.
# Idempotent; a doc that does not exist yet is linked anyway and shows up once created.
# Usage: link-obsidian.sh [vault]   (default: ~/Documents/obsidian/perso)
set -eu
vault=${1:-$HOME/Documents/obsidian/perso}
[ -d "$vault/.obsidian" ] || { echo "no Obsidian vault at $vault" >&2; exit 1; }
root=$(git rev-parse --show-toplevel)
target="$vault/$(basename "$root")"
mkdir -p "$target" "$root/docs"
for name in docs BACKLOG.md CHANGELOG.md GLOSSARY.md README.md; do
  ln -sfn "$root/$name" "$target/$name"
done
echo "linked $(basename "$root") into $target"
