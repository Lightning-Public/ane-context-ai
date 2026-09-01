import unittest

from ane_context_ai.review import (
    validate_context_promotion,
    validate_review_record,
    validate_source_pack_promotions,
)
from ane_context_ai.validation import ValidationError, validate_context_package


def human_approval() -> dict:
    return {
        "id": "review:human:001",
        "schema_version": "0.1.0",
        "created_at": "2026-08-21T08:00:00Z",
        "target": {
            "type": "context_package",
            "ids": ["package:001"],
        },
        "reviewer": {
            "identity_type": "human",
            "name": "Example Domain Reviewer",
            "identifier": "https://orcid.org/0000-0000-0000-0000",
            "role": "Assyriologist",
            "expertise": ["proto-cuneiform", "text edition"],
            "affiliation": "Example Institute",
        },
        "reviewed_at": "2026-08-21T08:00:00Z",
        "scope": {
            "evidence_ids": ["ev:001"],
            "artifact_ids": ["P000001"],
            "locators": ["obverse line 1"],
            "editions_consulted": [
                {"citation": "Example edition", "locator": "plate 1"}
            ],
        },
        "findings": [],
        "rights": {
            "attribution_checked": True,
            "reuse_checked": True,
            "notes": ["Attribution and reuse terms checked."],
        },
        "decision": "approve",
        "decision_notes": ["The cited line and claim classification were checked."],
        "signature": {
            "method": "orcid",
            "identifier": "https://orcid.org/0000-0000-0000-0000",
        },
    }


def package(status: str = "source_checked") -> dict:
    return {
        "id": "package:001",
        "schema_version": "0.1.0",
        "created_at": "2026-08-21T07:00:00Z",
        "question": {
            "original": "Question",
            "normalized": "Question",
            "scope": {
                "chronology": [],
                "places": [],
                "languages": [],
                "genres": [],
                "notes": [],
            },
        },
        "evidence": [
            {
                "id": "ev:001",
                "source": "Source",
                "source_record_id": "P000001",
                "stable_url": "https://example.test/P000001",
                "locator": "line 1",
                "layer": "transliteration",
                "excerpt": "X",
                "attribution": "Editor",
                "license_manifest_id": "license:001",
            }
        ],
        "claims": [
            {
                "id": "claim:001",
                "statement": "Claim",
                "status": "attested",
                "supporting_evidence_ids": ["ev:001"],
                "challenging_evidence_ids": [],
                "confidence": "high",
                "reasoning": "Direct metadata statement.",
            }
        ],
        "debates": [],
        "uncertainties": [],
        "bibliography": [],
        "retrieval": {
            "run_at": "2026-08-21T07:00:00Z",
            "source_manifest_ids": [],
            "queries": [],
            "software_version": "0.1.0",
            "model": None,
            "prompt_version": None,
        },
        "review": {
            "status": status,
            "reviewers": ["Example Domain Reviewer"] if status == "source_checked" else [],
            "review_record_ids": ["review:human:001"] if status == "source_checked" else [],
            "reviewed_at": "2026-08-21T08:00:00Z" if status == "source_checked" else None,
            "notes": [],
        },
    }


class ReviewRecordTests(unittest.TestCase):
    def test_human_approval_record_is_valid(self) -> None:
        validate_review_record(human_approval())

    def test_ai_cannot_approve(self) -> None:
        record = human_approval()
        record["reviewer"]["identity_type"] = "ai_assistant"
        with self.assertRaisesRegex(ValidationError, "only a human reviewer"):
            validate_review_record(record)

    def test_approval_requires_consulted_edition(self) -> None:
        record = human_approval()
        record["scope"]["editions_consulted"] = []
        with self.assertRaisesRegex(ValidationError, "consulted edition"):
            validate_review_record(record)

    def test_approval_rejects_blocking_finding(self) -> None:
        record = human_approval()
        record["findings"] = [
            {
                "kind": "disagreement",
                "summary": "Unresolved classification conflict.",
                "blocking": True,
                "evidence_ids": ["ev:001"],
                "represented_in": ["package#/uncertainties"],
            }
        ]
        with self.assertRaisesRegex(ValidationError, "blocking findings"):
            validate_review_record(record)


class ContextPromotionTests(unittest.TestCase):
    def test_source_checked_requires_review_metadata(self) -> None:
        value = package()
        value["review"]["review_record_ids"] = []
        with self.assertRaisesRegex(ValidationError, "review_record_ids"):
            validate_context_package(value)

    def test_human_approval_promotes_context_package(self) -> None:
        validate_context_promotion(package(), [human_approval()])

    def test_ai_audit_does_not_promote_context_package(self) -> None:
        record = human_approval()
        record["reviewer"]["identity_type"] = "ai_assistant"
        record["decision"] = "needs_revision"
        with self.assertRaisesRegex(ValidationError, "human approve"):
            validate_context_promotion(package(), [record])

    def test_approval_must_cover_all_evidence(self) -> None:
        value = package()
        value["evidence"].append(
            {
                **value["evidence"][0],
                "id": "ev:002",
                "source_record_id": "P000002",
            }
        )
        with self.assertRaisesRegex(ValidationError, "do not cover"):
            validate_context_promotion(value, [human_approval()])


class ArtifactPromotionTests(unittest.TestCase):
    def test_verified_artifact_requires_human_approval(self) -> None:
        record = human_approval()
        record["id"] = "review:artifact:001"
        record["target"] = {"type": "artifact", "ids": ["P000001"]}
        record["scope"]["artifact_ids"] = ["P000001"]
        manifest = {
            "objects": [
                {
                    "object_id": "P000001",
                    "status": "verified",
                    "verified_at": "2026-08-21T08:00:00Z",
                    "review_record_ids": ["review:artifact:001"],
                }
            ]
        }
        validate_source_pack_promotions(manifest, [record])

    def test_verified_artifact_rejects_missing_record(self) -> None:
        manifest = {
            "objects": [
                {
                    "object_id": "P000001",
                    "status": "verified",
                    "verified_at": "2026-08-21T08:00:00Z",
                    "review_record_ids": ["review:missing"],
                }
            ]
        }
        with self.assertRaisesRegex(ValidationError, "missing review records"):
            validate_source_pack_promotions(manifest, [])


if __name__ == "__main__":
    unittest.main()
