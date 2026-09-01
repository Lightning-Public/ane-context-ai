"""Build beginner-facing learning view models from Context Packages.

The view model is deliberately presentation-oriented but provenance-preserving:
source IDs, locators, review state, claim status, and uncertainty markers survive
unchanged while the raw research object is grouped for a learning interface.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .validation import HUMAN_REVIEWED_STATUSES, validate_context_package


REVIEW_PRESENTATION = {
    "unreviewed": {
        "label": "검토 전",
        "tone": "neutral",
        "message": "아직 사람의 사료 검토가 시작되지 않았습니다.",
    },
    "needs_revision": {
        "label": "수정 필요",
        "tone": "warning",
        "message": "출처는 연결되어 있지만 전문가가 해결해야 할 문제가 남아 있습니다.",
    },
    "source_checked": {
        "label": "사료 검토 완료",
        "tone": "positive",
        "message": "인용한 사료와 판본이 사람 검토를 통과했습니다.",
    },
    "expert_reviewed": {
        "label": "전문가 검토 완료",
        "tone": "positive",
        "message": "사료뿐 아니라 해석 범위까지 전문가 검토를 통과했습니다.",
    },
}

CLAIM_LANES = {
    "attested": {
        "id": "direct",
        "label": "자료가 직접 보여주는 것",
        "description": "현재 판본·메타데이터가 명시하는 내용입니다.",
    },
    "derived": {
        "id": "derived",
        "label": "자료 비교로 도출한 결론",
        "description": "여러 증거를 연결한 제한적 결론이며 직접 인용과 구분합니다.",
    },
    "scholarly_interpretation": {
        "id": "scholarship",
        "label": "현대 학자의 해석",
        "description": "연구자가 제안한 설명이며 다른 견해와 함께 읽어야 합니다.",
    },
    "model_inference": {
        "id": "model",
        "label": "AI 추론",
        "description": "탐색을 위한 가설이며 학술 근거로 자동 승격되지 않습니다.",
    },
}


def _evidence_reference(item: Mapping[str, Any]) -> dict[str, str]:
    return {
        "id": str(item["id"]),
        "record_id": str(item["source_record_id"]),
        "source": str(item["source"]),
        "url": str(item["stable_url"]),
        "locator": str(item["locator"]),
        "layer": str(item["layer"]),
    }


def _unique(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


def build_learning_view(package: Mapping[str, Any]) -> dict[str, Any]:
    """Return a serializable, provenance-preserving learning view model."""

    validate_context_package(package)

    evidence_items = list(package["evidence"])
    evidence_by_id = {str(item["id"]): item for item in evidence_items}

    artifacts_by_id: dict[str, dict[str, Any]] = {}
    secondary_sources: list[dict[str, Any]] = []
    for item in evidence_items:
        record_id = str(item["source_record_id"])
        layer = str(item["layer"])
        view_item = {
            **_evidence_reference(item),
            "excerpt": str(item["excerpt"]),
            "attribution": str(item["attribution"]),
            "license_manifest_id": str(item["license_manifest_id"]),
        }
        if record_id.startswith("P") and layer != "secondary":
            artifact = artifacts_by_id.setdefault(
                record_id,
                {
                    "id": record_id,
                    "source": str(item["source"]),
                    "url": str(item["stable_url"]),
                    "layers": [],
                },
            )
            artifact["layers"].append(view_item)
        else:
            secondary_sources.append(view_item)

    lanes = {
        lane["id"]: {**lane, "claims": []}
        for lane in CLAIM_LANES.values()
    }
    for claim in package["claims"]:
        status = str(claim["status"])
        lane = CLAIM_LANES[status]
        lanes[lane["id"]]["claims"].append(
            {
                "id": str(claim["id"]),
                "statement": str(claim["statement"]),
                "status": status,
                "confidence": str(claim["confidence"]),
                "reasoning": str(claim["reasoning"]),
                "supporting_evidence": [
                    _evidence_reference(evidence_by_id[evidence_id])
                    for evidence_id in claim["supporting_evidence_ids"]
                ],
                "challenging_evidence": [
                    _evidence_reference(evidence_by_id[evidence_id])
                    for evidence_id in claim["challenging_evidence_ids"]
                ],
            }
        )

    debates: list[dict[str, Any]] = []
    next_questions: list[str] = []
    for debate in package["debates"]:
        open_questions = [str(value) for value in debate["open_questions"]]
        next_questions.extend(open_questions)
        debates.append(
            {
                "issue": str(debate["issue"]),
                "positions": [
                    {
                        "summary": str(position["summary"]),
                        "evidence": [
                            _evidence_reference(evidence_by_id[evidence_id])
                            for evidence_id in position["evidence_ids"]
                        ],
                    }
                    for position in debate["positions"]
                ],
                "open_questions": open_questions,
            }
        )

    uncertainties = [
        {
            "target": str(item["target"]),
            "kind": str(item["kind"]),
            "description": str(item["description"]),
            "evidence": [
                _evidence_reference(evidence_by_id[evidence_id])
                for evidence_id in item["evidence_ids"]
            ],
        }
        for item in package["uncertainties"]
    ]

    review = package["review"]
    review_status = str(review["status"])
    review_presentation = REVIEW_PRESENTATION[review_status]
    scope = package["question"]["scope"]

    return {
        "id": str(package["id"]),
        "module": {
            "code": "ANE 101 · Module 3",
            "title": "도시와 문자의 탄생",
        },
        "question": {
            "original": str(package["question"]["original"]),
            "normalized": str(package["question"]["normalized"]),
        },
        "scope": {
            "chronology": [str(value) for value in scope["chronology"]],
            "places": [str(value) for value in scope["places"]],
            "languages": [str(value) for value in scope["languages"]],
            "genres": [str(value) for value in scope["genres"]],
            "notes": [str(value) for value in scope["notes"]],
        },
        "orientation": {
            "map_label": "우루크와 남부 메소포타미아 — 개념 지도, 축척 아님",
            "timeline": [
                {
                    "label": "Uruk IV",
                    "range": "ca. 3400–3200 BCE",
                    "role": "더 이른 기록 단계 — 다음 Source Pack에서 보강",
                    "active": False,
                },
                {
                    "label": "Uruk III",
                    "range": "ca. 3200–3000 BCE",
                    "role": "현재 세 자료가 속한 비교 범위",
                    "active": True,
                },
            ],
        },
        "artifacts": list(artifacts_by_id.values()),
        "secondary_sources": secondary_sources,
        "claim_lanes": list(lanes.values()),
        "debates": debates,
        "uncertainties": uncertainties,
        "review": {
            "status": review_status,
            "label": review_presentation["label"],
            "tone": review_presentation["tone"],
            "message": review_presentation["message"],
            "human_checked": review_status in HUMAN_REVIEWED_STATUSES,
            "reviewers": [str(value) for value in review["reviewers"]],
            "review_record_ids": [
                str(value) for value in review.get("review_record_ids", [])
            ],
            "reviewed_at": review.get("reviewed_at"),
            "notes": [str(value) for value in review["notes"]],
        },
        "provenance": {
            "created_at": str(package["created_at"]),
            "retrieved_at": str(package["retrieval"]["run_at"]),
            "source_manifest_ids": [
                str(value) for value in package["retrieval"]["source_manifest_ids"]
            ],
            "queries": [str(value) for value in package["retrieval"]["queries"]],
            "software_version": str(package["retrieval"]["software_version"]),
        },
        "next_questions": _unique(next_questions),
        "guardrails": [
            "resolved는 verified와 다릅니다.",
            "전사, 번역, 학술 해석, AI 설명을 같은 층위로 합치지 않습니다.",
            "손상·불확실성 기호를 지우거나 유창한 번역으로 가장하지 않습니다.",
            "현재 Uruk III 표본만으로 문자의 최초 발생 원인을 확정하지 않습니다.",
        ],
    }
