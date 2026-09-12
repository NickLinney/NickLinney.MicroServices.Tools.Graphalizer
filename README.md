# NickLinney Diagram Visualization Pipeline

`Graphalizer` is a Debian-first, Docker-only rendering pipeline for Mermaid and PlantUML source. The Sprint 1 vertical slice uses one shared Python standard-library core and direct renderer adapters to produce:

- `diagram.txt` — normalized UTF-8 source with LF line endings;
- `diagram.svg` — the canonical renderer output;
- `diagram.png` — derived from the SVG with librsvg; and
- `diagram.pdf` — derived from the SVG with librsvg.

Current lifecycle: development work for target `0.0.0-pre-alpha.1`. This repository is not released and makes no API-stability promise.

## Build

```sh
docker build --target runtime --tag nicklinney/graphalizer:0.0.0-dev .
```

The build pins the Debian base digest, PlantUML version and checksum, and Mermaid CLI version. See `DEPENDENCIES.md`.

## One-shot CLI

```sh
mkdir -p data/input data/output
cp tests/fixtures/small.mmd data/input/small.mmd

docker run --rm \
  --network none \
  --read-only \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --tmpfs /tmp:rw,nosuid,nodev,size=2g \
  --shm-size 2g \
  --memory 12g \
  --cpus 8 \
  --user "$(id -u):$(id -g)" \
  --volume "$PWD/data:/data" \
  nicklinney/graphalizer:0.0.0-dev \
  render \
  --engine mermaid \
  --input /data/input/small.mmd \
  --output /data/output/small-mermaid
```

Change the engine to `plantuml` and input to a `.puml` file for PlantUML. An existing output directory is never overwritten.

## Tests

Host-side unit tests require no third-party Python packages:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests/unit -v
```

The authoritative Sprint 1 renderer tests execute inside the same Debian image family:

```sh
docker build --target test --tag nicklinney/graphalizer-test:0.0.0-dev .
docker run --rm --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges \
  --tmpfs /tmp:rw,nosuid,nodev,size=2g \
  --shm-size 2g --memory 12g --cpus 8 \
  nicklinney/graphalizer-test:0.0.0-dev
```

## Sprint 1 boundary

The current slice does not include the HTTP API, artifact manifest, durable job state, atomic publication contract, remote storage validation, web UI, queue, release tag, or confidential large fixtures. See `ARCHITECTURE.md` and the outer project planning workspace.
