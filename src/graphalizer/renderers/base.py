"""Shared safe subprocess execution for renderer adapters."""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from graphalizer.errors import RenderError, RenderTimeoutError


MAX_DIAGNOSTIC_CHARACTERS = 16_384


@dataclass(frozen=True)
class CommandResult:
    stdout: str
    stderr: str
    duration_ms: int


def run_renderer_command(
    arguments: Sequence[str],
    *,
    cwd: Path,
    timeout_seconds: int,
    environment: Mapping[str, str] | None = None,
) -> CommandResult:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            list(arguments),
            cwd=cwd,
            env=dict(environment) if environment is not None else None,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        raise RenderTimeoutError(f"renderer exceeded {timeout_seconds} seconds") from exc
    except OSError as exc:
        raise RenderError(f"renderer could not start: {exc}") from exc

    duration_ms = round((time.monotonic() - started) * 1000)
    stdout = completed.stdout[-MAX_DIAGNOSTIC_CHARACTERS:]
    stderr = completed.stderr[-MAX_DIAGNOSTIC_CHARACTERS:]
    if completed.returncode != 0:
        detail = stderr.strip() or stdout.strip() or "no diagnostics"
        raise RenderError(f"renderer exited {completed.returncode}: {detail}")
    return CommandResult(stdout=stdout, stderr=stderr, duration_ms=duration_ms)


def read_version(arguments: Sequence[str], *, cwd: Path, environment: Mapping[str, str] | None = None) -> str:
    result = run_renderer_command(arguments, cwd=cwd, timeout_seconds=30, environment=environment)
    version = (result.stdout.strip() or result.stderr.strip()).splitlines()
    return version[0] if version else "unknown"
