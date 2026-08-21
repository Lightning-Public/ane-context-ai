"""Dependency-free semantic checks for Context Packages.

JSON Schema remains the shape contract. These checks cover cross-references that
are easier to express in code and can run before a schema dependency is chosen.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class ValidationError(ValueError):
    """Raised when a Context Package violates a core project invariant."""


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


def validate_context_package(package: Mapping[str, Any]) -> None:
    """Validate required fields, unique IDs, and evidence references."""

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
