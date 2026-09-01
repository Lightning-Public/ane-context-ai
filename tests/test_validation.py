import json
import unittest
from copy import deepcopy
from pathlib import Path

from ane_context_ai.validation import ValidationError, validate_context_package


ROOT = Path(__file__).resolve().parents[1]


class ContextPackageValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.example = json.loads(
            (ROOT / "examples" / "context-package.example.json").read_text(encoding="utf-8")
        )
        cls.r002_draft = json.loads(
            (ROOT / "examples" / "r002-origin-of-writing.context-package.json").read_text(
                encoding="utf-8"
            )
        )

    def test_example_is_valid(self) -> None:
        validate_context_package(self.example)

    def test_r002_draft_is_valid(self) -> None:
        validate_context_package(self.r002_draft)

    def test_r002_source_audit_keeps_needs_revision(self) -> None:
        self.assertEqual(self.r002_draft["review"]["status"], "needs_revision")
        self.assertTrue(self.r002_draft["review"]["reviewers"])

    def test_r002_transliteration_uncertainty_markers_are_preserved(self) -> None:
        excerpts = {item["id"]: item["excerpt"] for item in self.r002_draft["evidence"]}
        self.assertIn(
            "|SZE~a&SZE~a|#?",
            excerpts["ev:cdli:P002718:transliteration"],
        )
        self.assertIn(
            "U4 SZUBUR#",
            excerpts["ev:cdli:P000014:transliteration"],
        )
        self.assertIn(
            "U4# |KAK~a.GA2~a1|",
            excerpts["ev:cdli:P000021:transliteration"],
        )

    def test_r002_records_p002718_classification_uncertainty(self) -> None:
        uncertainties = {
            item["target"]: item["description"] for item in self.r002_draft["uncertainties"]
        }
        self.assertIn("P002718 genre classification", uncertainties)
        self.assertIn("Geography 5", uncertainties["P002718 genre classification"])

    def test_unknown_evidence_reference_is_rejected(self) -> None:
        package = deepcopy(self.example)
        package["claims"][0]["supporting_evidence_ids"] = ["ev:missing"]

        with self.assertRaisesRegex(ValidationError, "unknown evidence ids"):
            validate_context_package(package)

    def test_duplicate_evidence_ids_are_rejected(self) -> None:
        package = deepcopy(self.example)
        package["evidence"].append(deepcopy(package["evidence"][0]))

        with self.assertRaisesRegex(ValidationError, "must be unique"):
            validate_context_package(package)


if __name__ == "__main__":
    unittest.main()
