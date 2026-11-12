#!/bin/sh
# GitHub side of an sdlc project. Needs gh, authenticated.
#   - main: no force-push, no deletion; direct pushes stay allowed (trunk-based);
#   - Dependabot alerts and security update PRs on.
# Each step reports its own failure (a private repo on a free plan refuses rulesets).
set -u
command -v gh >/dev/null || { echo "gh is not installed: skipped GitHub setup" >&2; exit 1; }
repo=$(gh repo view --json nameWithOwner -q .nameWithOwner) || exit 1
status=0
if gh api -X POST "repos/$repo/rulesets" --input - >/dev/null <<JSON
{
  "name": "sdlc: protect main",
  "target": "branch",
  "enforcement": "active",
  "conditions": {"ref_name": {"include": ["refs/heads/main"], "exclude": []}},
  "rules": [{"type": "deletion"}, {"type": "non_fast_forward"}]
}
JSON
then echo "main protected on $repo (no force-push, no deletion)"
else echo "could not protect main on $repo" >&2; status=1
fi
if gh api -X PUT "repos/$repo/vulnerability-alerts" >/dev/null &&
  gh api -X PUT "repos/$repo/automated-security-fixes" >/dev/null; then
  echo "Dependabot alerts and security updates on for $repo"
else echo "could not turn on Dependabot alerts on $repo" >&2; status=1
fi
exit $status
