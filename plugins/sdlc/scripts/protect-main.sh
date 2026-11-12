#!/bin/sh
# Light protection of main on GitHub: no force-push, no deletion. Direct pushes
# stay allowed so trunk-based work keeps working. Needs gh, authenticated.
set -e
command -v gh >/dev/null || { echo "gh is not installed: skipped main protection" >&2; exit 1; }
repo=$(gh repo view --json nameWithOwner -q .nameWithOwner)
gh api -X POST "repos/$repo/rulesets" --input - <<JSON
{
  "name": "sdlc: protect main",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["refs/heads/main"], "exclude": []}},
  "rules": [{"type": "deletion"}, {"type": "non_fast_forward"}]
}
JSON
echo "main protected on $repo (no force-push, no deletion)"
