# Security Posture

This Sprint 1 implementation is intended for local, bounded rendering of trusted or owner-controlled diagram source.

- Run without runtime network access.
- Run as a non-root user.
- Drop Linux capabilities and set `no-new-privileges`.
- Keep the root filesystem read-only and use an isolated temporary filesystem.
- Limit the container to 256 processes and disable additional swap beyond its 12 GiB memory limit.
- PlantUML uses its `SECURE` security profile.
- Only fixed renderer arguments are exposed; subprocesses never use a shell.
- Input is strict UTF-8, NUL-free, and limited to 5 MiB.
- Output destinations are never overwritten.

The checked Puppeteer configuration requests Chromium `--no-sandbox` and `--disable-setuid-sandbox` because the non-root, capability-dropped, no-new-privileges envelope cannot start Chromium's setuid/user-namespace sandbox on the current Docker Desktop runtime. This is an explicit Sprint 1 exception: it is acceptable only for trusted/local-controlled inputs inside the remaining boundary—no network, non-root execution, read-only root filesystem, all Linux capabilities dropped, `no-new-privileges`, bounded temporary storage, and explicit CPU, memory, swap, and process limits. It avoids granting `SYS_ADMIN`, running as root, or using privileged mode. It is not an untrusted-input, public, or multi-tenant security claim. A future hardened deployment must restore Chromium sandboxing or obtain a new Security/Operations disposition.

Do not put credentials, private keys, PAT files, or confidential large fixtures inside this repository, build context, image, logs, or evidence artifacts.

The Sprint 1 slice does not claim untrusted-input, public-network, multi-tenant, denial-of-service, crash-safe persistence, or remote-include acceptance.
