"""Dependency-free semantic checks for Context Packages.

JSON Schema remains the shape contract. These checks cover cross-references and
promotion invariants that are easier to express in code.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Any


class ValidationError(ValueError):
    """Raised when a project artifact violates a core invariant."""


REQUIRED_TOP_LEVEL = {
    "id",
    "schema_version",
    "created_at",
    "question",
    "evidence",
    "claims",
    "debates",
    "uncertainties",
    "bibliography",
    "retrieval",
    "review",
}

HUMAN_REVIEWED_STATUSES = {"source_checked", "expert_reviewed"}
REVIEW_STATUSES = {
    "unreviewed",
    "source_checked",
    "expert_reviewed",
    "needs_revision",
}


def _ids(items: list[Mapping[str, Any]], label: str) -> set[str]:
    values: list[str] = []
    for index, item in enumerate(items):
        value = item.get("id")
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(f"{label}[{index}].id must be a non-empty string")
        values.append(value)
    if len(values) != len(set(values)):
        raise ValidationError(f"{label} ids must be unique")
    return set(values)


def _require_known_ids(values: Any, known: set[str], path: str) -> None:
    if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
        raise ValidationError(f"{path} must be a list of strings")
    missing = sorted(set(values) - known)
    if missing:
        raise ValidationError(f"{path} references unknown evidence ids: {missing}")


def _nonempty_strings(values: Any, path: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(values, list) or not all(
        isinstance(value, str) and value.strip() for value in values
    ):
        raise ValidationError(f"{path} must be a list of non-empty strings")
    if not allow_empty and not values:
        raise ValidationError(f"{path} must not be empty")
    if len(values) != len(set(values)):
        raise ValidationError(f"{path} values must be unique")
    return values


def _validate_datetime(value: Any, path: str, *, allow_none: bool = False) -> None:
    if value is None and allow_none:
        return
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{path} must be an RFC-3339 date-time string")
    candidate = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise ValidationError(f"{path} must be an RFC-3339 date-time string") from exc
    if parsed.tzinfo is None:
        raise ValidationError(f"{path} must include a UTC offset")


def validate_context_package(package: Mapping[str, Any]) -> None:
    """Validate required fields, references, and review-state invariants."""

    if not isinstance(package, Mapping):
        raise ValidationError("package must be a JSON object")

    missing_fields = sorted(REQUIRED_TOP_LEVEL - package.keys())
    if missing_fields:
        raise ValidationError(f"missing top-level fields: {missing_fields}")

    if package.get("schema_version") != "0.1.0":
        raise ValidationError("schema_version must be 0.1.0")

    evidence = package.get("evidence")
    claims = package.get("claims")
    if not isinstance(evidence, list) or not all(isinstance(item, Mapping) for item in evidence):
        raise ValidationError("evidence must be a list of objects")
    if not isinstance(claims, list) or not all(isinstance(item, Mapping) for item in claims):
        raise ValidationError("claims must be a list of objects")

    evidence_ids = _ids(evidence, "evidence")
    _ids(claims, "claims")

    for index, claim in enumerate(claims):
        _require_known_ids(
            claim.get("supporting_evidence_ids"),
            evidence_ids,
            f"claims[{index}].supporting_evidence_ids",
        )
        _require_known_ids(
            claim.get("challenging_evidence_ids"),
            evidence_ids,
            f"claims[{index}].challenging_evidence_ids",
        )

    uncertainties = package.get("uncertainties")
    if not isinstance(uncertainties, list) or not all(
        isinstance(item, Mapping) for item in uncertainties
    ):
        raise ValidationError("uncertainties must be a list of objects")
    for index, uncertainty in enumerate(uncertainties):
        _require_known_ids(
            uncertainty.get("evidence_ids"),
            evidence_ids,
            f"uncertainties[{index}].evidence_ids",
        )

    review = package.get("review")
    if not isinstance(review, Mapping):
        raise ValidationError("review must be an object")
    status = review.get("status")
    if status not in REVIEW_STATUSES:
        raise ValidationError(f"review.status must be one of {sorted(REVIEW_STATUSES)}")

    reviewers = _nonempty_strings(review.get("reviewers"), "review.reviewers")
    _nonempty_strings(review.get("notes"), "review.notes")

    review_record_ids = review.get("review_record_ids", [])
    _nonempty_strings(review_record_ids, "review.review_record_ids")
    reviewed_at = review.get("reviewed_at")
    _validate_datetime(reviewed_at, "review.reviewed_at", allow_none=True)

    if status in HUMAN_REVIEWED_STATUSES:
        if not reviewers:
            raise ValidationError(
                f"review.reviewers must not be empty when status is {status}"
            )
        if not review_record_ids:
            raise ValidationError(
                f"review.review_record_ids must not be empty when status is {status}"
            )
        if reviewed_at is None:
            raise ValidationError(
                f"review.reviewed_at is required when status is {status}"
            )
