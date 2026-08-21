import json
import unittest
from pathlib import Path

from ane_context_ai.learning_view import build_learning_view


ROOT = Path(__file__).resolve().parents[1]


class LearningViewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.package = json.loads(
            (ROOT / "examples" / "r002-origin-of-writing.context-package.json").read_text(
                encoding="utf-8"
            )
        )
        cls.view = build_learning_view(cls.package)

    def test_review_state_is_visible_without_false_promotion(self) -> None:
        self.assertEqual(self.view["review"]["status"], "needs_revision")
        self.assertEqual(self.view["review"]["label"], "수정 필요")
        self.assertFalse(self.view["review"]["human_checked"])

    def test_artifacts_are_grouped_by_stable_record_id(self) -> None:
        artifact_ids = {artifact["id"] for artifact in self.view["artifacts"]}
        self.assertEqual(artifact_ids, {"P002718", "P000014", "P000021"})
        for artifact in self.view["artifacts"]:
            layers = {layer["layer"] for layer in artifact["layers"]}
            self.assertIn("artifact", layers)
            self.assertIn("transliteration", layers)

    def test_damage_and_uncertainty_markers_survive(self) -> None:
        excerpts = "\n".join(
            layer["excerpt"]
            for artifact in self.view["artifacts"]
            for layer in artifact["layers"]
            if layer["layer"] == "transliteration"
        )
        self.assertIn("#?", excerpts)
        self.assertIn("[...]", excerpts)
        self.assertIn(" X", excerpts)

    def test_claims_are_split_into_epistemic_lanes(self) -> None:
        lanes = {lane["id"]: lane for lane in self.view["claim_lanes"]}
        self.assertGreaterEqual(len(lanes["direct"]["claims"]), 1)
        self.assertGreaterEqual(len(lanes["derived"]["claims"]), 1)
        self.assertGreaterEqual(len(lanes["scholarship"]["claims"]), 1)

    def test_every_claim_reference_keeps_url_and_locator(self) -> None:
        references = [
            reference
            for lane in self.view["claim_lanes"]
            for claim in lane["claims"]
            for key in ("supporting_evidence", "challenging_evidence")
            for reference in claim[key]
        ]
        self.assertTrue(references)
        self.assertTrue(all(reference["url"] for reference in references))
        self.assertTrue(all(reference["locator"] for reference in references))

    def test_view_model_is_json_serializable(self) -> None:
        rendered = json.dumps(self.view, ensure_ascii=False)
        self.assertIn("문자는 왜 탄생했는가?", rendered)


if __name__ == "__main__":
    unittest.main()
