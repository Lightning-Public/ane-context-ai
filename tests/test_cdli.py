import unittest

from ane_context_ai.cdli import (
    CDLIClient,
    CDLIError,
    artifact_api_url,
    artifact_numeric_id,
    normalize_artifact_metadata,
    normalize_p_number,
    verify_candidate,
)
from ane_context_ai.cdli_manifest import verify_manifest


SAMPLE_RECORD = {
    "id": 6427,
    "period": {"name": "Uruk III"},
    "provenience": {"name": "Uruk (mod. Warka)"},
    "genres": [{"name": "Administrative"}],
    "collections": [{"name": "Vorderasiatisches Museum, Berlin"}],
    "museum_no": "W 00000",
    "publications": [{"designation": "Sample publication"}],
    "inscription": {"id": 123},
}


class CDLIHelpersTests(unittest.TestCase):
    def test_p_number_normalization_and_route(self) -> None:
        self.assertEqual(normalize_p_number("p006427"), "P006427")
        self.assertEqual(artifact_numeric_id("P006427"), 6427)
        self.assertEqual(
            artifact_api_url("P006427"),
            "https://cdli.earth/artifacts/6427.json",
        )

    def test_invalid_p_number_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            normalize_p_number("6427")

    def test_nested_metadata_is_extracted_without_inference(self) -> None:
        metadata = normalize_artifact_metadata("P006427", SAMPLE_RECORD)

        self.assertEqual(metadata["period"], "Uruk III")
        self.assertEqual(metadata["provenience"], "Uruk (mod. Warka)")
        self.assertEqual(metadata["genre"], "Administrative")
        self.assertEqual(metadata["collection"], "Vorderasiatisches Museum, Berlin")
        self.assertEqual(metadata["museum_no"], "W 00000")
        self.assertEqual(metadata["publications"], ["Sample publication"])
        self.assertTrue(metadata["inscription_availability"])
        self.assertIn("period", metadata["response_fields"])

    def test_live_style_single_item_array_is_unwrapped(self) -> None:
        client = CDLIClient(transport=lambda _url, _timeout: [SAMPLE_RECORD])
        metadata = client.get_artifact("P006427")

        self.assertEqual(metadata["object_id"], "P006427")
        self.assertEqual(metadata["period"], "Uruk III")

    def test_ambiguous_array_is_rejected(self) -> None:
        client = CDLIClient(transport=lambda _url, _timeout: [SAMPLE_RECORD, SAMPLE_RECORD])

        with self.assertRaisesRegex(CDLIError, "expected exactly one artifact"):
            client.get_artifact("P006427")


class CDLIVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.urls: list[str] = []

        def transport(url: str, timeout: float):
            self.urls.append(url)
            self.assertEqual(timeout, 3.0)
            return [SAMPLE_RECORD]

        self.client = CDLIClient(timeout=3.0, transport=transport)

    def test_candidate_is_resolved_but_not_silently_promoted(self) -> None:
        result = verify_candidate(
            {"object_id": "P006427", "period": "Uruk III", "status": "candidate"},
            self.client,
        )

        self.assertEqual(result["status"], "candidate")
        self.assertEqual(result["verification"]["status"], "resolved")
        self.assertTrue(result["verification"]["period_matches_candidate"])
        self.assertEqual(self.urls, ["https://cdli.earth/artifacts/6427.json"])

    def test_manifest_records_timestamp_and_counts(self) -> None:
        manifest = {
            "manifest_version": "0.1.0",
            "objects": [
                {"object_id": "P006427", "period": "Uruk III", "status": "candidate"},
                {"object_id": "P006428", "period": "Uruk III", "status": "candidate"},
            ],
        }
        result = verify_manifest(
            manifest,
            self.client,
            retrieved_at="2026-08-21T05:00:00+00:00",
        )

        self.assertEqual(result["verification_run"]["attempted"], 2)
        self.assertEqual(result["verification_run"]["resolved"], 2)
        self.assertEqual(result["verification_run"]["errors"], 0)
        self.assertEqual(
            result["objects"][0]["verification"]["retrieved_at"],
            "2026-08-21T05:00:00+00:00",
        )


if __name__ == "__main__":
    unittest.main()
