from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from graphalizer.application import render
from graphalizer.contracts import Engine, RenderRequest
from graphalizer.errors import RenderError


FIXTURES = Path(__file__).parents[1] / "fixtures"


@unittest.skipUnless(os.environ.get("GRAPHALIZER_INTEGRATION") == "1", "container integration test")
class PlantUmlIntegrationTests(unittest.TestCase):
    def test_valid_plantuml_produces_complete_artifact_family(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "result"
            result = render(RenderRequest(Engine.PLANTUML, FIXTURES / "small.puml", output, 120))
            self.assertEqual({artifact.format for artifact in result.artifacts}, {"txt", "svg", "png", "pdf"})
            self.assertTrue(all(artifact.size_bytes > 0 for artifact in result.artifacts))

    def test_invalid_plantuml_does_not_publish_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "result"
            with self.assertRaises(RenderError):
                render(RenderRequest(Engine.PLANTUML, FIXTURES / "invalid.puml", output, 120))
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
