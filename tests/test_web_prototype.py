import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web" / "r002"


class WebPrototypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = (WEB / "index.html").read_text(encoding="utf-8")
        cls.css = (WEB / "styles.css").read_text(encoding="utf-8")
        cls.javascript = (WEB / "app.js").read_text(encoding="utf-8")

    def test_semantic_landmarks_exist(self) -> None:
        self.assertIn('<html lang="ko">', self.html)
        for section_id in (
            "orientation",
            "artifacts",
            "claims",
            "debates",
            "uncertainties",
            "provenance",
            "next-questions",
        ):
            self.assertIn(f'id="{section_id}"', self.html)

    def test_prototype_uses_repository_fixture(self) -> None:
        self.assertIn(
            "../../examples/r002-origin-of-writing.context-package.json",
            self.javascript,
        )

    def test_renderer_avoids_untrusted_html_injection(self) -> None:
        self.assertNotIn("innerHTML", self.javascript)
        self.assertIn("textContent", self.javascript)

    def test_no_restricted_external_images_are_embedded(self) -> None:
        self.assertNotIn("<img", self.html.lower())
        self.assertIn("개념 지도", self.html)

    def test_responsive_rules_exist(self) -> None:
        self.assertIn("@media (max-width: 760px)", self.css)
        self.assertIn("prefers-reduced-motion", self.css)


if __name__ == "__main__":
    unittest.main()
