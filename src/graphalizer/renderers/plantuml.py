"""Direct PlantUML command-line adapter."""

from __future__ import annotations

import os
from pathlib import Path

from graphalizer.contracts import AdapterResult
from graphalizer.errors import RenderError
from graphalizer.renderers.base import read_version, run_renderer_command


class PlantUmlAdapter:
    def __init__(self, jar_path: Path | None = None) -> None:
        self.jar_path = jar_path or Path(os.environ.get("PLANTUML_JAR", "/opt/plantuml/plantuml.jar"))

    def render_svg(self, source_path: Path, work_directory: Path, timeout_seconds: int) -> AdapterResult:
        output_directory = work_directory / "plantuml-output"
        output_directory.mkdir()
        environment = os.environ.copy()
        environment["PLANTUML_SECURITY_PROFILE"] = "SECURE"
        command = [
            "java",
            "-Djava.awt.headless=true",
            "-DPLANTUML_SECURITY_PROFILE=SECURE",
            "-jar",
            str(self.jar_path),
            "-failfast2",
            "-tsvg",
            "-o",
            output_directory.name,
            source_path.name,
        ]
        result = run_renderer_command(
            command,
            cwd=source_path.parent,
            timeout_seconds=timeout_seconds,
            environment=environment,
        )
        svg_path = output_directory / f"{source_path.stem}.svg"
        if not svg_path.is_file() or svg_path.stat().st_size == 0:
            raise RenderError("PlantUML did not produce a non-empty SVG")
        version = read_version(
            ["java", "-jar", str(self.jar_path), "-version"],
            cwd=work_directory,
            environment=environment,
        )
        diagnostics = tuple(line for line in (result.stderr.strip(), result.stdout.strip()) if line)
        return AdapterResult(svg_path, version, result.duration_ms, diagnostics)
