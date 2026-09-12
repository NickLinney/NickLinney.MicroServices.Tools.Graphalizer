"""Direct Mermaid CLI adapter."""

from __future__ import annotations

import os
from pathlib import Path

from graphalizer.contracts import AdapterResult
from graphalizer.errors import RenderError
from graphalizer.renderers.base import read_version, run_renderer_command


class MermaidAdapter:
    def render_svg(self, source_path: Path, work_directory: Path, timeout_seconds: int) -> AdapterResult:
        svg_path = work_directory / "mermaid-output.svg"
        environment = os.environ.copy()
        environment.setdefault("PUPPETEER_EXECUTABLE_PATH", "/usr/bin/chromium")
        command = [
            "mmdc",
            "--input",
            str(source_path),
            "--output",
            str(svg_path),
            "--backgroundColor",
            "transparent",
            "--puppeteerConfigFile",
            "/opt/graphalizer/puppeteer-config.json",
        ]
        result = run_renderer_command(
            command,
            cwd=work_directory,
            timeout_seconds=timeout_seconds,
            environment=environment,
        )
        if not svg_path.is_file() or svg_path.stat().st_size == 0:
            raise RenderError("Mermaid CLI did not produce a non-empty SVG")
        version = read_version(["mmdc", "--version"], cwd=work_directory, environment=environment)
        diagnostics = tuple(line for line in (result.stderr.strip(), result.stdout.strip()) if line)
        return AdapterResult(svg_path, version, result.duration_ms, diagnostics)
