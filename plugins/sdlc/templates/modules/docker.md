### Module: docker

Pushing a `vX.Y.Z` tag builds the root `Dockerfile` and publishes `ghcr.io/<owner>/<repo>:X.Y.Z` (`.github/workflows/docker.yml`). Write the Dockerfile when it is first needed: multi-stage, minimal runtime image, no secrets baked in.
