"""Minimal provenance-first client for verifying CDLI artifact metadata."""

from __future__ import annotations

import json
import re
from collections.abc import Callable, Mapping, Sequence
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


P_NUMBER_RE = re.compile(r"^P(?P<number>\d{6,})$")
DEFAULT_BASE_URL = "https://cdli.earth/"
USER_AGENT = "ane-context-ai/0.1 (+https://github.com/Lightning-Public/ane-context-ai)"


class CDLIError(RuntimeError):
    """Raised when CDLI metadata cannot be fetched or interpreted."""


def normalize_p_number(value: str) -> str:
    """Return a canonical CDLI P-number or raise ValueError."""

    candidate = value.strip().upper()
    match = P_NUMBER_RE.fullmatch(candidate)
    if not match:
        raise ValueError(f"invalid CDLI P-number: {value!r}")
    return f"P{match.group('number')}"


def artifact_numeric_id(p_number: str) -> int:
    """Convert P006427 to the numeric artifact id used by CDLI routes."""

    canonical = normalize_p_number(p_number)
    return int(canonical[1:])


def artifact_api_url(p_number: str, base_url: str = DEFAULT_BASE_URL) -> str:
    """Build the documented JSON metadata URL for a CDLI artifact."""

    return urljoin(base_url.rstrip("/") + "/", f"artifacts/{artifact_numeric_id(p_number)}.json")


def artifact_page_url(p_number: str, base_url: str = DEFAULT_BASE_URL) -> str:
    """Build the human-facing stable CDLI P-number URL."""

    canonical = normalize_p_number(p_number)
    return urljoin(base_url.rstrip("/") + "/", canonical)


def _http_get_json(url: str, timeout: float) -> Mapping[str, Any]:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed HTTPS authority by default
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise CDLIError(f"CDLI returned HTTP {exc.code} for {url}") from exc
    except URLError as exc:
        raise CDLIError(f"CDLI request failed for {url}: {exc.reason}") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CDLIError(f"CDLI returned invalid JSON for {url}") from exc

    if not isinstance(payload, Mapping):
        raise CDLIError(f"CDLI returned a non-object JSON payload for {url}")
    return payload


def _key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def _display(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (str, int, float)):
        text = str(value).strip()
        return text or None
    if isinstance(value, Mapping):
        for name in ("name", "label", "designation", "title", "value"):
            if name in value:
                rendered = _display(value[name])
                if rendered:
                    return rendered
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for item in value:
            rendered = _display(item)
            if rendered:
                return rendered
    return None


def _walk_mapping(value: Any):
    if isinstance(value, Mapping):
        for key, child in value.items():
            yield str(key), child
            yield from _walk_mapping(child)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for child in value:
            yield from _walk_mapping(child)


def _first(record: Mapping[str, Any], aliases: set[str]) -> str | None:
    normalized = {_key(alias) for alias in aliases}
    for key, value in _walk_mapping(record):
        if _key(key) in normalized:
            rendered = _display(value)
            if rendered:
                return rendered
    return None


def _all(record: Mapping[str, Any], aliases: set[str]) -> list[str]:
    normalized = {_key(alias) for alias in aliases}
    values: list[str] = []
    for key, value in _walk_mapping(record):
        if _key(key) not in normalized:
            continue
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            for item in value:
                rendered = _display(item)
                if rendered and rendered not in values:
                    values.append(rendered)
        else:
            rendered = _display(value)
            if rendered and rendered not in values:
                values.append(rendered)
    return values


def _has_nonempty(record: Mapping[str, Any], aliases: set[str]) -> bool:
    normalized = {_key(alias) for alias in aliases}
    for key, value in _walk_mapping(record):
        if _key(key) in normalized and value not in (None, "", [], {}):
            return True
    return False


def normalize_artifact_metadata(
    p_number: str,
    record: Mapping[str, Any],
    *,
    base_url: str = DEFAULT_BASE_URL,
) -> dict[str, Any]:
    """Extract conservative, non-inferred fields from a CDLI artifact response.

    The raw response is intentionally retained because CDLI's schema can evolve.
    Missing fields remain null/empty rather than being guessed.
    """

    canonical = normalize_p_number(p_number)
    return {
        "object_id": canonical,
        "stable_url": artifact_page_url(canonical, base_url),
        "api_url": artifact_api_url(canonical, base_url),
        "period": _first(record, {"period", "period_name", "periodName"}),
        "provenience": _first(
            record, {"provenience", "provenience_name", "provenienceName", "provenance"}
        ),
        "genre": _first(record, {"genre", "genre_name", "genreName", "genres"}),
        "collection": _first(
            record, {"collection", "collection_name", "collectionName", "collections"}
        ),
        "museum_no": _first(
            record, {"museum_no", "museum_number", "museumNumber", "museum_numbers"}
        ),
        "publications": _all(record, {"publication", "publications", "designation"}),
        "inscription_availability": _has_nonempty(
            record, {"inscription", "inscriptions", "transliteration", "transcription"}
        ),
        "raw": dict(record),
    }


class CDLIClient:
    """Small injectable client used by the batch verifier and unit tests."""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        *,
        timeout: float = 20.0,
        transport: Callable[[str, float], Mapping[str, Any]] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout
        self.transport = transport or _http_get_json

    def get_artifact(self, p_number: str) -> dict[str, Any]:
        canonical = normalize_p_number(p_number)
        url = artifact_api_url(canonical, self.base_url)
        record = self.transport(url, self.timeout)
        return normalize_artifact_metadata(canonical, record, base_url=self.base_url)


def verify_candidate(
    candidate: Mapping[str, Any],
    client: CDLIClient,
) -> dict[str, Any]:
    """Verify one manifest candidate without silently promoting it."""

    object_id = candidate.get("object_id")
    if not isinstance(object_id, str):
        raise ValueError("candidate.object_id must be a string")

    result = dict(candidate)
    try:
        metadata = client.get_artifact(object_id)
    except (ValueError, CDLIError) as exc:
        result["verification"] = {
            "status": "error",
            "error": str(exc),
        }
        return result

    expected_period = candidate.get("period")
    actual_period = metadata.get("period")
    period_matches = None
    if isinstance(expected_period, str) and isinstance(actual_period, str):
        period_matches = _key(expected_period) == _key(actual_period)

    result["verification"] = {
        "status": "resolved",
        "period_matches_candidate": period_matches,
        "metadata": metadata,
        "missing_fields": [
            field
            for field in ("period", "provenience", "genre")
            if not metadata.get(field)
        ],
    }
    return result
