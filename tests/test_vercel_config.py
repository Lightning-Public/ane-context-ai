import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VercelConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))

    def test_static_site_serves_from_repository_root(self) -> None:
        self.assertEqual(self.config.get("outputDirectory"), ".")
        self.assertNotIn("functions", self.config)
        self.assertNotIn("builds", self.config)

    def test_root_and_learning_routes_target_existing_prototype(self) -> None:
        rewrites = {
            item["source"]: item["destination"]
            for item in self.config.get("rewrites", [])
        }
        expected = "/web/r002/index.html"
        self.assertEqual(rewrites.get("/"), expected)
        self.assertEqual(rewrites.get("/learn/origin-of-writing"), expected)
        self.assertTrue((ROOT / expected.lstrip("/")).is_file())

    def test_context_package_fixture_remains_deployable(self) -> None:
        self.assertTrue(
            (ROOT / "examples" / "r002-origin-of-writing.context-package.json").is_file()
        )


if __name__ == "__main__":
    unittest.main()
