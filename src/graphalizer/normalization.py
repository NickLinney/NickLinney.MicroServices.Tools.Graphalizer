"""Truthful cross-engine text normalization."""

from __future__ import annotations

import hashlib
from pathlib import Path

from graphalizer.contracts import NormalizedSource
from graphalizer.errors import InputError


DEFAULT_MAX_INPUT_BYTES = 5 * 1024 * 1024


def normalize_source(path: Path, max_bytes: int = DEFAULT_MAX_INPUT_BYTES) -> NormalizedSource:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise InputError(f"cannot read input: {exc}") from exc

    if not raw:
        raise InputError("input is empty")
    if len(raw) > max_bytes:
        raise InputError(f"input exceeds {max_bytes} bytes")
    if b"\x00" in raw:
        raise InputError("input contains a NUL byte")

    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise InputError("input must be valid UTF-8") from exc

    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n"
    normalized = normalized_text.encode("utf-8")
    return NormalizedSource(
        content=normalized,
        original_sha256=hashlib.sha256(raw).hexdigest(),
        normalized_sha256=hashlib.sha256(normalized).hexdigest(),
    )
