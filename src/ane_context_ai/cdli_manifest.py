"""Batch verification helpers for CDLI-backed source-pack manifests."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from .cdli import CDLIClient, verify_candidate


def verify_manifest(
    manifest: Mapping[str, Any],
    client: CDLIClient,
    *,
    limit: int | None = None,
    retrieved_at: str | None = None,
) -> dict[str, Any]:
    """Return a copy of a source-pack manifest with CDLI verification results."""

    objects = manifest.get("objects")
    if not isinstance(objects, list) or not all(isinstance(item, Mapping) for item in objects):
        raise ValueError("manifest.objects must be a list of objects")
    if limit is not None and limit < 1:
        raise ValueError("limit must be at least 1")

    timestamp = retrieved_at or datetime.now(timezone.utc).isoformat()
    selected = objects if limit is None else objects[:limit]
    verified: list[dict[str, Any]] = []

    for candidate in selected:
        result = verify_candidate(candidate, client)
        verification = result.setdefault("verification", {})
        verification["retrieved_at"] = timestamp
        verified.append(result)

    output = dict(manifest)
    if limit is None:
        output["objects"] = verified
    else:
        output["objects"] = verified + [dict(item) for item in objects[limit:]]

    statuses = [item.get("verification", {}).get("status") for item in verified]
    output["verification_run"] = {
        "source": "CDLI",
        "retrieved_at": timestamp,
        "attempted": len(verified),
        "resolved": statuses.count("resolved"),
        "errors": statuses.count("error"),
        "limit": limit,
    }
    return output
