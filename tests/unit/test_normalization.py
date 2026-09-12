from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from graphalizer.errors import InputError
from graphalizer.normalization import normalize_source


class NormalizeSourceTests(unittest.TestCase):
    def normalize(self, content: bytes):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "source.txt"
            path.write_bytes(content)
            return normalize_source(path)

    def test_normalizes_bom_and_mixed_line_endings(self) -> None:
        original = b"\xef\xbb\xbfline one\r\nline two\rline three\n\n"
        result = self.normalize(original)
        self.assertEqual(result.content, b"line one\nline two\nline three\n")
        self.assertEqual(result.original_sha256, hashlib.sha256(original).hexdigest())
        self.assertEqual(result.normalized_sha256, hashlib.sha256(result.content).hexdigest())

    def test_preserves_spaces_and_internal_blank_lines(self) -> None:
        result = self.normalize(b"  first  \n\n  second\t\n")
        self.assertEqual(result.content, b"  first  \n\n  second\t\n")

    def test_rejects_empty_input(self) -> None:
        with self.assertRaises(InputError):
            self.normalize(b"")

    def test_rejects_invalid_utf8(self) -> None:
        with self.assertRaises(InputError):
            self.normalize(b"\xff")

    def test_rejects_nul(self) -> None:
        with self.assertRaises(InputError):
            self.normalize(b"valid\x00invalid")

    def test_rejects_input_over_limit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "source.txt"
            path.write_bytes(b"abcd")
            with self.assertRaises(InputError):
                normalize_source(path, max_bytes=3)


if __name__ == "__main__":
    unittest.main()
