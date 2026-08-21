"""Human review records and promotion gates.

Machine resolution and AI-assisted audits may record findings, but only an
attributable human approval record can promote a Context Package to
``source_checked``/``expert_reviewed`` or an artifact to ``verified``.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Any

from .validation import (
    HUMAN_REVIEWED_STATUSES,
    ValidationError,
    validate_context_package,
)


REVIEW_DECISIONS = {"approve", "needs_revision", "reject"}
REVIEWER_TYPES = {"human", "ai_assistant"}
TARGET_TYPES = {"context_package", "artifact"}
FINDING_KINDS = {
    "agreement",
    "correction",
    "disagreement",
    "rights",
    "limitation",
    "other",
}
SIGNATURE_METHODS = {
    "github_account",
    "github_issue",
    "git_commit",
    "orcid",
    "other",
}


def _require_mapping(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValidationError(f"{path} must be an object")
    return value


def _require_string(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{path} must be a non-empty string")
    return value


def _require_strings(
    value: Any,
    path: str,
    *,
    allow_empty: bool = True,
) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise ValidationError(f"{path} must be a list of non-empty strings")
    if not allow_empty and not value:
        raise ValidationError(f"{path} must not be empty")
    if len(value) != len(set(value)):
        raise ValidationError(f"{path} values must be unique")
    return value


def _parse_datetime(value: Any, path: str) -> datetime:
    text = _require_string(value, path)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"{path} must be an RFC-3339 date-time string") from exc
    if parsed.tzinfo is None:
        raise ValidationError(f"{path} must include a UTC offset")
    return parsed


def _record_id(record: Mapping[str, Any]) -> str:
    return _require_string(record.get("id"), "review_record.id")


def validate_review_record(record: Mapping[str, Any]) -> None:
    """Validate one machine-readable review record."""

    record = _require_mapping(record, "review_record")
    required = {
        "id",
        "schema_version",
        "created_at",
        "target",
        "reviewer",
        "reviewed_at",
        "scope",
        "findings",
        "rights",
        "decision",
        "decision_notes",
        "signature",
    }
    missing = sorted(required - record.keys())
    if missing:
        raise ValidationError(f"review record missing fields: {missing}")

    _record_id(record)
    if record.get("schema_version") != "0.1.0":
        raise ValidationError("review_record.schema_version must be 0.1.0")
    _parse_datetime(record.get("created_at"), "review_record.created_at")
    _parse_datetime(record.get("reviewed_at"), "review_record.reviewed_at")

    target = _require_mapping(record.get("target"), "review_record.target")
    if target.get("type") not in TARGET_TYPES:
        raise ValidationError(
            f"review_record.target.type must be one of {sorted(TARGET_TYPES)}"
        )
    target_ids = _require_strings(
        target.get("ids"),
        "review_record.target.ids",
        allow_empty=False,
    )

    reviewer = _require_mapping(record.get("reviewer"), "review_record.reviewer")
    reviewer_type = reviewer.get("identity_type")
    if reviewer_type not in REVIEWER_TYPES:
        raise ValidationError(
            f"review_record.reviewer.identity_type must be one of {sorted(REVIEWER_TYPES)}"
        )
    _require_string(reviewer.get("name"), "review_record.reviewer.name")
    _require_string(reviewer.get("role"), "review_record.reviewer.role")
    _require_strings(
        reviewer.get("expertise"),
        "review_record.reviewer.expertise",
        allow_empty=False,
    )
    identifier = reviewer.get("identifier")
    if identifier is not None:
        _require_string(identifier, "review_record.reviewer.identifier")
    affiliation = reviewer.get("affiliation")
    if affiliation is not None:
        _require_string(affiliation, "review_record.reviewer.affiliation")

    scope = _require_mapping(record.get("scope"), "review_record.scope")
    evidence_ids = _require_strings(
        scope.get("evidence_ids"),
        "review_record.scope.evidence_ids",
    )
    artifact_ids = _require_strings(
        scope.get("artifact_ids"),
        "review_record.scope.artifact_ids",
    )
    _require_strings(scope.get("locators"), "review_record.scope.locators")

    editions = scope.get("editions_consulted")
    if not isinstance(editions, list) or not all(
        isinstance(item, Mapping) for item in editions
    ):
        raise ValidationError(
            "review_record.scope.editions_consulted must be a list of objects"
        )
    for index, edition in enumerate(editions):
        _require_string(
            edition.get("citation"),
            f"review_record.scope.editions_consulted[{index}].citation",
        )
        _require_string(
            edition.get("locator"),
            f"review_record.scope.editions_consulted[{index}].locator",
        )

    if target.get("type") == "artifact":
        missing_artifacts = sorted(set(target_ids) - set(artifact_ids))
        if missing_artifacts:
            raise ValidationError(
                "artifact review target ids must also appear in "
                f"review_record.scope.artifact_ids: {missing_artifacts}"
            )

    findings = record.get("findings")
    if not isinstance(findings, list) or not all(
        isinstance(item, Mapping) for item in findings
    ):
        raise ValidationError("review_record.findings must be a list of objects")

    blocking_findings = 0
    for index, finding in enumerate(findings):
        kind = finding.get("kind")
        if kind not in FINDING_KINDS:
            raise ValidationError(
                f"review_record.findings[{index}].kind must be one of "
                f"{sorted(FINDING_KINDS)}"
            )
        _require_string(
            finding.get("summary"),
            f"review_record.findings[{index}].summary",
        )
        blocking = finding.get("blocking")
        if not isinstance(blocking, bool):
            raise ValidationError(
                f"review_record.findings[{index}].blocking must be boolean"
            )
        if blocking:
            blocking_findings += 1
        finding_evidence = _require_strings(
            finding.get("evidence_ids"),
            f"review_record.findings[{index}].evidence_ids",
        )
        represented_in = _require_strings(
            finding.get("represented_in"),
            f"review_record.findings[{index}].represented_in",
        )
        unknown = sorted(set(finding_evidence) - set(evidence_ids))
        if unknown:
            raise ValidationError(
                f"review_record.findings[{index}].evidence_ids are outside "
                f"the reviewed scope: {unknown}"
            )
        if kind == "disagreement" and not blocking and not represented_in:
            raise ValidationError(
                "non-blocking disagreements must name where they remain visible "
                f"at review_record.findings[{index}].represented_in"
            )

    rights = _require_mapping(record.get("rights"), "review_record.rights")
    for field in ("attribution_checked", "reuse_checked"):
        if not isinstance(rights.get(field), bool):
            raise ValidationError(f"review_record.rights.{field} must be boolean")
    _require_strings(rights.get("notes"), "review_record.rights.notes")

    decision = record.get("decision")
    if decision not in REVIEW_DECISIONS:
        raise ValidationError(
            f"review_record.decision must be one of {sorted(REVIEW_DECISIONS)}"
        )
    _require_strings(
        record.get("decision_notes"),
        "review_record.decision_notes",
        allow_empty=False,
    )

    signature = _require_mapping(record.get("signature"), "review_record.signature")
    method = signature.get("method")
    if method not in SIGNATURE_METHODS:
        raise ValidationError(
            f"review_record.signature.method must be one of {sorted(SIGNATURE_METHODS)}"
        )
    _require_string(signature.get("identifier"), "review_record.signature.identifier")

    if decision == "approve":
        if reviewer_type != "human":
            raise ValidationError("only a human reviewer may issue an approve decision")
        if not editions:
            raise ValidationError(
                "approve decisions require at least one consulted edition/source"
            )
        if not evidence_ids and not artifact_ids:
            raise ValidationError(
                "approve decisions require reviewed evidence_ids or artifact_ids"
            )
        if not rights.get("attribution_checked") or not rights.get("reuse_checked"):
            raise ValidationError(
                "approve decisions require attribution and reuse checks"
            )
        if blocking_findings:
            raise ValidationError(
                "approve decisions cannot contain blocking findings"
            )


def _review_record_map(
    records: list[Mapping[str, Any]],
) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for record in records:
        validate_review_record(record)
        record_id = _record_id(record)
        if record_id in result:
            raise ValidationError(f"duplicate review record id: {record_id}")
        result[record_id] = record
    return result


def validate_context_promotion(
    package: Mapping[str, Any],
    review_records: list[Mapping[str, Any]],
) -> None:
    """Require attributable human approval for promoted Context Packages."""

    validate_context_package(package)
    review = _require_mapping(package.get("review"), "review")
    status = review.get("status")
    if status not in HUMAN_REVIEWED_STATUSES:
        raise ValidationError(
            "context package is not in a human-reviewed promotion state"
        )

    record_ids = _require_strings(
        review.get("review_record_ids"),
        "review.review_record_ids",
        allow_empty=False,
    )
    records = _review_record_map(review_records)
    missing = sorted(set(record_ids) - set(records))
    if missing:
        raise ValidationError(f"missing referenced review records: {missing}")

    package_id = _require_string(package.get("id"), "package.id")
    approval_records: list[Mapping[str, Any]] = []
    for record_id in record_ids:
        record = records[record_id]
        target = _require_mapping(record.get("target"), "review_record.target")
        if target.get("type") != "context_package" or package_id not in target.get("ids", []):
            raise ValidationError(
                f"review record {record_id} does not target context package {package_id}"
            )
        reviewer = _require_mapping(record.get("reviewer"), "review_record.reviewer")
        if (
            record.get("decision") == "approve"
            and reviewer.get("identity_type") == "human"
        ):
            approval_records.append(record)

    if not approval_records:
        raise ValidationError(
            "source_checked/expert_reviewed requires at least one human approve record"
        )

    package_evidence = {
        _require_string(item.get("id"), "evidence.id")
        for item in package.get("evidence", [])
    }
    reviewed_evidence: set[str] = set()
    approval_names: set[str] = set()
    latest_reviewed_at: datetime | None = None
    for record in approval_records:
        reviewer = _require_mapping(record.get("reviewer"), "review_record.reviewer")
        approval_names.add(_require_string(reviewer.get("name"), "reviewer.name"))
        scope = _require_mapping(record.get("scope"), "review_record.scope")
        reviewed_evidence.update(scope.get("evidence_ids", []))
        reviewed_at = _parse_datetime(record.get("reviewed_at"), "review_record.reviewed_at")
        if latest_reviewed_at is None or reviewed_at > latest_reviewed_at:
            latest_reviewed_at = reviewed_at

    uncovered = sorted(package_evidence - reviewed_evidence)
    if uncovered:
        raise ValidationError(
            f"human approval records do not cover package evidence ids: {uncovered}"
        )

    display_reviewers = set(review.get("reviewers", []))
    missing_names = sorted(approval_names - display_reviewers)
    if missing_names:
        raise ValidationError(
            f"review.reviewers omits approving human reviewers: {missing_names}"
        )

    package_reviewed_at = _parse_datetime(review.get("reviewed_at"), "review.reviewed_at")
    if latest_reviewed_at is not None and package_reviewed_at < latest_reviewed_at:
        raise ValidationError(
            "review.reviewed_at cannot predate the latest approving review record"
        )


def validate_source_pack_promotions(
    manifest: Mapping[str, Any],
    review_records: list[Mapping[str, Any]],
) -> None:
    """Require human artifact reviews for every ``verified`` source-pack record."""

    manifest = _require_mapping(manifest, "source_pack")
    objects = manifest.get("objects")
    if not isinstance(objects, list) or not all(
        isinstance(item, Mapping) for item in objects
    ):
        raise ValidationError("source_pack.objects must be a list of objects")

    records = _review_record_map(review_records)
    for index, item in enumerate(objects):
        if item.get("status") != "verified":
            continue
        object_id = _require_string(
            item.get("object_id"),
            f"source_pack.objects[{index}].object_id",
        )
        _parse_datetime(
            item.get("verified_at"),
            f"source_pack.objects[{index}].verified_at",
        )
        record_ids = _require_strings(
            item.get("review_record_ids"),
            f"source_pack.objects[{index}].review_record_ids",
            allow_empty=False,
        )
        missing = sorted(set(record_ids) - set(records))
        if missing:
            raise ValidationError(
                f"verified artifact {object_id} references missing review records: {missing}"
            )

        approved = False
        for record_id in record_ids:
            record = records[record_id]
            target = _require_mapping(record.get("target"), "review_record.target")
            reviewer = _require_mapping(record.get("reviewer"), "review_record.reviewer")
            if (
                target.get("type") == "artifact"
                and object_id in target.get("ids", [])
                and record.get("decision") == "approve"
                and reviewer.get("identity_type") == "human"
            ):
                approved = True
                break
        if not approved:
            raise ValidationError(
                f"verified artifact {object_id} lacks a human approve record"
            )
