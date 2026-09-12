"""SVG validation and pinned librsvg conversion adapter."""

from __future__ import annotations

import subprocess
from pathlib import Path
from xml.etree import ElementTree

from graphalizer.errors import ConversionError, RenderTimeoutError


MAX_DIAGNOSTIC_CHARACTERS = 16_384


def validate_svg(path: Path) -> None:
    try:
        root = ElementTree.parse(path).getroot()
    except (OSError, ElementTree.ParseError) as exc:
        raise ConversionError(f"invalid SVG output: {exc}") from exc
    if root.tag.rsplit("}", 1)[-1] != "svg":
        raise ConversionError("renderer output root is not SVG")


def convert_svg(source: Path, destination: Path, output_format: str, timeout_seconds: int) -> None:
    if output_format not in {"png", "pdf"}:
        raise ConversionError(f"unsupported conversion format: {output_format}")
    command = [
        "rsvg-convert",
        "--format",
        output_format,
        "--keep-aspect-ratio",
        "--output",
        str(destination),
        str(source),
    ]
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        raise RenderTimeoutError(f"{output_format} conversion exceeded {timeout_seconds} seconds") from exc
    except OSError as exc:
        raise ConversionError(f"converter could not start: {exc}") from exc
    if completed.returncode != 0:
        diagnostics = (completed.stderr or completed.stdout)[-MAX_DIAGNOSTIC_CHARACTERS:].strip()
        raise ConversionError(f"{output_format} conversion exited {completed.returncode}: {diagnostics}")
    if not destination.is_file() or destination.stat().st_size == 0:
        raise ConversionError(f"converter did not produce a non-empty {output_format} file")


def validate_signature(path: Path, output_format: str) -> None:
    expected = {"png": b"\x89PNG\r\n\x1a\n", "pdf": b"%PDF-"}[output_format]
    try:
        prefix = path.read_bytes()[: len(expected)]
    except OSError as exc:
        raise ConversionError(f"cannot validate {output_format}: {exc}") from exc
    if prefix != expected:
        raise ConversionError(f"output does not have a valid {output_format} signature")
