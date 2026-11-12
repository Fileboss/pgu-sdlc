### Module: ci

`.github/workflows/ci.yml` runs `make lint test` on pushes to `main` and on pull requests. Keep CI calling the Makefile, never tools directly; when a stack needs a new setup step, add it to the workflow.
