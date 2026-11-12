#!/bin/sh
# Vendor the selected skills of github.com/mattpocock/skills (MIT) into the plugin,
# pinned to one commit. Review `git diff plugins/sdlc/skills` before committing.
# Usage: scripts/sync-pocock.sh [ref]   (default: the upstream default branch)
#
# Transforms, applied on every sync:
#   - skills calling each other by bare name ("tdd") are pointed at the plugin
#     namespace ("sdlc:tdd"); "code-review" stays bare: it is Claude Code's built-in;
#   - phase skills that sdlc drives (to-spec, to-tickets, grill-with-docs) lose
#     `disable-model-invocation`, so /sdlc:next and autonomous runs can call them;
#   - Codex metadata (agents/openai.yaml) is dropped.
set -eu
ref=${1:-HEAD}
skills="productivity/grilling engineering/grill-with-docs engineering/domain-modeling
engineering/to-spec engineering/to-tickets engineering/tdd engineering/pr
productivity/handoff engineering/retro engineering/diagnosing-bugs
engineering/prototype engineering/codebase-design productivity/writing-for-agents"
model_invoked="to-spec to-tickets grill-with-docs"

root=$(cd "$(dirname "$0")/.." && pwd)
dest=$root/plugins/sdlc/skills
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

git clone -q https://github.com/mattpocock/skills "$tmp/upstream"
git -C "$tmp/upstream" checkout -q "$ref"
sha=$(git -C "$tmp/upstream" rev-parse HEAD)

rm -rf "$dest"
mkdir -p "$dest"
names=""
for path in $skills; do
  name=$(basename "$path")
  names="$names $name"
  cp -R "$tmp/upstream/skills/$path" "$dest/$name"
  rm -rf "$dest/$name/agents"
done

for name in $names; do
  for file in $(find "$dest" -name '*.md'); do
    NAME=$name perl -pi -e 'my $n = $ENV{NAME};
      s/(["`])\Q$n\E\1/${1}sdlc:$n$1/g if /Skill tool/;
      s/the `\Q$n\E` skill/the `sdlc:$n` skill/g' "$file"
  done
done
for name in $model_invoked; do
  perl -ni -e 'print unless /^disable-model-invocation: true$/' "$dest/$name/SKILL.md"
done

cp "$tmp/upstream/LICENSE" "$dest/LICENSE-mattpocock"
cat > "$dest/VENDORED.md" <<MD
# Vendored skills

Copied from https://github.com/mattpocock/skills (MIT, see LICENSE-mattpocock)
at commit \`$sha\` by \`scripts/sync-pocock.sh\`. Do not edit here: change the
script's transforms or the selection, then re-run \`make sync-pocock\`.

Skills:$names
MD
echo "vendored $sha into plugins/sdlc/skills:$names"
