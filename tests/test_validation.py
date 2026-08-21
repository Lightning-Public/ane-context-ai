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
