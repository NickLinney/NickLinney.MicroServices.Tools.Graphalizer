# Security Posture

This Sprint 1 implementation is intended for local, bounded rendering of potentially untrusted diagram source.

- Run without runtime network access.
- Run as a non-root user.
- Drop Linux capabilities and set `no-new-privileges`.
- Keep the root filesystem read-only and use an isolated temporary filesystem.
- PlantUML uses its `SECURE` security profile.
- Only fixed renderer arguments are exposed; subprocesses never use a shell.
- Input is strict UTF-8, NUL-free, and limited to 5 MiB.
- Output destinations are never overwritten.

The checked Puppeteer configuration does not request `--no-sandbox`. If Mermaid cannot execute without privileged mode, broad capabilities, root, or disabling Chromium's sandbox, stop the affected acceptance path and obtain a Security/Operations disposition rather than weakening the container silently.

Do not put credentials, private keys, PAT files, or confidential large fixtures inside this repository, build context, image, logs, or evidence artifacts.

The Sprint 1 slice does not claim public-network, multi-tenant, denial-of-service, crash-safe persistence, or remote-include acceptance.
