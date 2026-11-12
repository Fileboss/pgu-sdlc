.PHONY: sync-pocock validate test

# Re-vendor Matt Pocock's skills; pass REF=<sha|branch> to pin another commit.
sync-pocock:
	scripts/sync-pocock.sh $(REF)
	git diff --stat -- plugins/sdlc/skills

validate:
	claude plugin validate .
	claude plugin validate plugins/sdlc

# The mod's tests (band, commit gate), run by Claude Code's plugin test kit.
test:
	claude plugin test plugins/sdlc
