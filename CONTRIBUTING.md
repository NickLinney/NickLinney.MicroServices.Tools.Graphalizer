# Contributing

Development occurs on bounded `feature/*` branches. Sprint 1 work targets `feature/renderer-vertical-slice`, which may merge only into `release/pre-alpha/1` after review. Do not push, promote, tag, or release without the accountable gate disposition.

Before requesting review:

1. Run the host-side unit suite.
2. Run the Docker integration suite with runtime networking disabled.
3. Confirm `git status` contains no credentials, private fixtures, generated data, or unrelated changes.
4. Record the exact commit and image identity for any evidence claim.
