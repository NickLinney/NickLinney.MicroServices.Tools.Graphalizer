# Architecture

## Sprint 1 vertical slice

```text
CLI -> RenderRequest -> application.render
                         |-> normalized UTF-8/LF diagram.txt
                         |-> MermaidAdapter  -> SVG
                         |-> PlantUmlAdapter -> SVG
                         `-> rsvg-convert -> PNG + PDF
```

The command line is an entry-point adapter. It contains no rendering rules. `application.render` is the shared use case that a future HTTP adapter will call.

Renderer processes are invoked with argument arrays through `subprocess.run`; no shell interprets source, paths, or renderer options. Only the two enumerated engines and the fixed adapter options are accepted.

## Decisions implemented

- Direct Mermaid CLI and PlantUML adapters; no Kroki dependency.
- One non-root Debian application image for both current CLI and future API modes.
- `diagram.txt` means normalized source for both engines.
- SVG is the candidate canonical rendered form; PNG and PDF are produced by librsvg.
- Original-byte and normalized-byte hashes are separate facts.
- Runtime network access is not required for the checked fixtures.

## Deliberate limitations

Sprint 1 publication is all-or-none in the ordinary success path because conversions finish in a temporary directory before the destination is created. It is not yet the manifest-last, same-filesystem, crash-safe atomic protocol required for MVP acceptance.

The large-fixture run is architecture evidence only. Formal large-input acceptance follows implementation of resource policy, the artifact manifest, and atomic storage behavior.
