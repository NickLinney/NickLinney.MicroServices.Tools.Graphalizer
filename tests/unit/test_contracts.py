from __future__ import annotations

import unittest
from pathlib import Path

from graphalizer.contracts import Engine, RenderRequest


class ContractTests(unittest.TestCase):
    def test_render_request_is_engine_neutral(self) -> None:
        request = RenderRequest(Engine.MERMAID, Path("input.mmd"), Path("output"), 30)
        self.assertEqual(request.engine.value, "mermaid")
        self.assertEqual(request.timeout_seconds, 30)


if __name__ == "__main__":
    unittest.main()
