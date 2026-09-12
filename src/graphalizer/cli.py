"""Parameterized one-shot command-line entry point."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from graphalizer import __version__
from graphalizer.application import render
from graphalizer.contracts import Engine, RenderRequest, RenderResult
from graphalizer.errors import GraphalizerError


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="graphalizer")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    render_parser = commands.add_parser("render", help="render one Mermaid or PlantUML source")
    render_parser.add_argument("--engine", choices=[engine.value for engine in Engine], required=True)
    render_parser.add_argument("--input", type=Path, required=True)
    render_parser.add_argument("--output", type=Path, required=True)
    render_parser.add_argument("--timeout", type=int, default=600)
    return parser


def _serialize(result: RenderResult) -> dict[str, object]:
    return {
        "status": "completed",
        "engine": result.engine.value,
        "engineVersion": result.engine_version,
        "originalSha256": result.original_sha256,
        "normalizedSha256": result.normalized_sha256,
        "durationMs": result.duration_ms,
        "artifacts": [
            {
                "format": artifact.format,
                "path": str(artifact.path),
                "bytes": artifact.size_bytes,
                "sha256": artifact.sha256,
            }
            for artifact in result.artifacts
        ],
        "diagnostics": list(result.diagnostics),
    }


def main(arguments: list[str] | None = None) -> int:
    args = _parser().parse_args(arguments)
    if args.command != "render":
        return 64
    try:
        result = render(
            RenderRequest(
                engine=Engine(args.engine),
                input_path=args.input,
                output_directory=args.output,
                timeout_seconds=args.timeout,
            )
        )
    except GraphalizerError as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}), file=sys.stderr)
        return exc.exit_code
    print(json.dumps(_serialize(result), indent=2, sort_keys=True))
    return 0
