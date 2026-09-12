"""Engine-neutral contracts used by both the CLI and future API adapter."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Protocol


class Engine(str, Enum):
    MERMAID = "mermaid"
    PLANTUML = "plantuml"


@dataclass(frozen=True)
class NormalizedSource:
    content: bytes
    original_sha256: str
    normalized_sha256: str


@dataclass(frozen=True)
class RenderRequest:
    engine: Engine
    input_path: Path
    output_directory: Path
    timeout_seconds: int = 600


@dataclass(frozen=True)
class AdapterResult:
    svg_path: Path
    engine_version: str
    duration_ms: int
    diagnostics: tuple[str, ...] = ()


@dataclass(frozen=True)
class ArtifactResult:
    format: str
    path: Path
    size_bytes: int
    sha256: str


@dataclass(frozen=True)
class RenderResult:
    engine: Engine
    engine_version: str
    original_sha256: str
    normalized_sha256: str
    duration_ms: int
    artifacts: tuple[ArtifactResult, ...]
    diagnostics: tuple[str, ...] = ()


class RendererAdapter(Protocol):
    def render_svg(self, source_path: Path, work_directory: Path, timeout_seconds: int) -> AdapterResult:
        """Render normalized source to SVG inside work_directory."""
