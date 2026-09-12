"""Engine-neutral rendering use case shared by all entry points."""

from __future__ import annotations

import hashlib
import shutil
import tempfile
import time
from pathlib import Path

from graphalizer.contracts import ArtifactResult, Engine, RenderRequest, RenderResult, RendererAdapter
from graphalizer.conversion import convert_svg, validate_signature, validate_svg
from graphalizer.errors import InputError, StorageError
from graphalizer.normalization import normalize_source
from graphalizer.renderers import MermaidAdapter, PlantUmlAdapter


def _adapter_for(engine: Engine) -> RendererAdapter:
    if engine is Engine.MERMAID:
        return MermaidAdapter()
    if engine is Engine.PLANTUML:
        return PlantUmlAdapter()
    raise InputError(f"unsupported engine: {engine}")


def _artifact(path: Path, output_format: str) -> ArtifactResult:
    with path.open("rb") as artifact_file:
        digest = hashlib.file_digest(artifact_file, "sha256").hexdigest()
    return ArtifactResult(
        format=output_format,
        path=path,
        size_bytes=path.stat().st_size,
        sha256=digest,
    )


def render(request: RenderRequest) -> RenderResult:
    if request.timeout_seconds < 1:
        raise InputError("timeout must be at least one second")
    if request.output_directory.exists():
        raise StorageError("output directory already exists; refusing to overwrite it")
    if not request.input_path.is_file():
        raise InputError("input path is not a regular file")

    normalized = normalize_source(request.input_path)
    adapter = _adapter_for(request.engine)
    started = time.monotonic()

    with tempfile.TemporaryDirectory(prefix="graphalizer-") as temporary:
        work_directory = Path(temporary)
        extension = ".mmd" if request.engine is Engine.MERMAID else ".puml"
        normalized_path = work_directory / f"source{extension}"
        normalized_path.write_bytes(normalized.content)

        adapter_result = adapter.render_svg(
            normalized_path,
            work_directory,
            request.timeout_seconds,
        )
        validate_svg(adapter_result.svg_path)

        staged_txt = work_directory / "diagram.txt"
        staged_svg = work_directory / "diagram.svg"
        staged_png = work_directory / "diagram.png"
        staged_pdf = work_directory / "diagram.pdf"
        staged_txt.write_bytes(normalized.content)
        if adapter_result.svg_path != staged_svg:
            shutil.copyfile(adapter_result.svg_path, staged_svg)
        convert_svg(staged_svg, staged_png, "png", request.timeout_seconds)
        convert_svg(staged_svg, staged_pdf, "pdf", request.timeout_seconds)
        validate_signature(staged_png, "png")
        validate_signature(staged_pdf, "pdf")

        try:
            request.output_directory.mkdir(parents=True, exist_ok=False)
            final_paths: list[tuple[str, Path]] = []
            for output_format, staged in (
                ("txt", staged_txt),
                ("svg", staged_svg),
                ("png", staged_png),
                ("pdf", staged_pdf),
            ):
                destination = request.output_directory / staged.name
                shutil.copyfile(staged, destination)
                final_paths.append((output_format, destination))
        except OSError as exc:
            raise StorageError(f"cannot publish output: {exc}") from exc

    duration_ms = round((time.monotonic() - started) * 1000)
    return RenderResult(
        engine=request.engine,
        engine_version=adapter_result.engine_version,
        original_sha256=normalized.original_sha256,
        normalized_sha256=normalized.normalized_sha256,
        duration_ms=duration_ms,
        artifacts=tuple(_artifact(path, output_format) for output_format, path in final_paths),
        diagnostics=adapter_result.diagnostics,
    )
