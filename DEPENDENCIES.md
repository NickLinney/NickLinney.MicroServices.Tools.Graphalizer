# Dependency and Runtime Baseline

## Directly pinned build inputs

| Component | Pin | Integrity source | Purpose |
|---|---|---|---|
| Debian | `13-slim@sha256:d7e12182ce18b85b93007c1dedf31f2d29e01ccf3182cc4017c709b6259bc132` | Docker Hub content digest resolved 2026-09-12 | Runtime base |
| PlantUML | `1.2026.8` | Release JAR SHA-256 `5e1ecfa8ecd32c90b03bbf3b1eb6f020943f98ab0fcf4032be31a0002ee2c462` | PlantUML SVG rendering |
| Mermaid CLI | `11.16.0` | Exact npm package version | Mermaid SVG rendering |
| Puppeteer | `24.31.0` | Exact npm package version | Node 20-compatible Chromium control for Mermaid CLI |

PlantUML version and checksum come from the official GitHub release. Mermaid CLI version comes from the official project release. The build must fail if the PlantUML checksum differs.

Mermaid CLI permits Puppeteer 23, 24, or 25. Puppeteer 25 requires Node 22.12 or later, while Debian 13 supplies Node 20. The explicit Puppeteer 24.31.0 pin prevents npm from resolving the incompatible Puppeteer 25 peer dependency and supports Node 18 or later.

## Debian-provided runtime dependencies

The image installs Chromium, the default headless Java runtime, Graphviz, librsvg, Node.js, Python 3, Tini, GNU time, Fontconfig, DejaVu fonts, and Liberation fonts from the pinned Debian base's configured repositories. Exact resolved package versions must be captured from the built image with:

```sh
dpkg-query -W -f='${Package}\t${Version}\n' | sort
```

Mermaid's npm dependency closure must be captured with `npm list --global --all` before release evidence is accepted.

## Licensing qualification

All selected components are intended to be FLOSS, but this development baseline is not a completed legal or release license review. The Security/Release dependency task must bind the exact resolved transitive inventory, licenses, and image identity before `0.0.0-pre-alpha.1` can be released.
