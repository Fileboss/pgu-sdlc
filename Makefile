.PHONY: sync-pocock validate

# Re-vendor Matt Pocock's skills; pass REF=<sha|branch> to pin another commit.
sync-pocock:
	scripts/sync-pocock.sh $(REF)
	git diff --stat -- plugins/sdlc/skills

validate:
	claude plugin validate .
	claude plugin validate plugins/sdlc
