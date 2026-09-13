# Context Package → Research Space 매핑

## 목적

`schemas/context-package.schema.json`의 학술적 층위를 훼손하지 않고, Context Package를 Research Space에서 탐색 가능한 노드/엣지 그래프로 투영한다.

이 변환은 **read-only projection**이다. 원본 Context Package를 수정하지 않는다.

## 핵심 원칙

1. 원본 ID를 보존한다.
2. 증거와 해석을 같은 노드 타입으로 평탄화하지 않는다.
3. 불확실성을 삭제하거나 숫자 신뢰도로 임의 환산하지 않는다.
4. `supporting_evidence_ids`와 `challenging_evidence_ids`를 명시적 관계로 보존한다.
5. Debate의 position은 Claim과 동일시하지 않고 별도 `position` 노드로 유지한다.
6. Review/Retrieval은 연구 내용이 아니라 provenance 메타데이터로 표시한다.

## 노드 매핑

| Context Package | Research Space node | 설명 |
| --- | --- | --- |
| `question` | `question` | 원 질문과 정규화 질문, scope를 함께 보존 |
| `evidence[]` | `evidence` | layer, locator, stable_url, attribution 포함 |
| `claims[]` | `claim` | status와 confidence를 그대로 표시 |
| `debates[]` | `debate` | 논쟁 issue 자체 |
| `debates[].positions[]` | `position` | 논쟁 내 대안 해석 |
| `debates[].open_questions[]` | `question` | 미해결 질문 |
| `uncertainties[]` | `uncertainty` | kind, target, description 보존 |
| `bibliography[]` | `source` | 서지 정보와 URL |
| `retrieval` | `provenance` | 검색 시점, query, software/model/prompt 버전 |
| `review` | `review` | 검토 상태와 reviewer/notes |

## 엣지 매핑

| 원본 관계 | Research Space edge |
| --- | --- |
| claim.supporting_evidence_ids | `supports` : evidence → claim |
| claim.challenging_evidence_ids | `challenges` : evidence → claim |
| debate.positions | `has_position` : debate → position |
| position.evidence_ids | `supported_by` : position → evidence |
| debate.open_questions | `opens` : debate → question |
| uncertainty.evidence_ids | `grounded_in` : uncertainty → evidence |
| uncertainty.target | 가능한 경우 target node에 `qualifies` 연결, 해석 불가 시 문자열 target 보존 |
| bibliography | 직접 참조 ID가 스키마에 없으므로 v0.1에서는 독립 source node |
| retrieval/review | package root와 `provenance_of`, `review_of` 관계 |

## UI 표현 규칙

### Evidence layer

다음 layer는 색/배지로 구분하되 타입은 모두 `evidence`로 유지한다.

- artifact
- image
- transliteration
- translation
- edition
- secondary

### Claim status

- `attested`: 직접 증거에 의해 확인되는 주장
- `derived`: 증거에서 도출된 주장
- `scholarly_interpretation`: 학술 해석
- `model_inference`: AI 추론

`model_inference`는 다른 claim보다 시각적으로 강하게 구분하며, 검토 전에는 사실로 표현하지 않는다.

### Uncertainty

`reading`, `translation`, `identity`, `chronology`, `provenience`, `interpretation`, `coverage`, `other`를 제거하거나 하나의 confidence 값으로 축약하지 않는다.

## 변환 결과 계약

```json
{
  "packageId": "example:synthetic:001",
  "schemaVersion": "0.1.0",
  "nodes": [
    {
      "id": "question:root",
      "type": "question",
      "label": "합성 예시 문헌은 무엇을 보여 주는가?",
      "data": {}
    }
  ],
  "edges": [
    {
      "id": "edge:ev:001:supports:claim:001",
      "from": "ev:001",
      "to": "claim:001",
      "relation": "supports"
    }
  ],
  "meta": {
    "createdAt": "...",
    "reviewStatus": "source_checked"
  }
}
```

## v0.1 비범위

- UI에서 원본 Context Package 직접 수정
- uncertainty → 단일 confidence score 자동 변환
- bibliography와 claim의 자동 의미 연결
- debate position을 정식 claim으로 승격
- 서로 다른 Context Package 간 graph merge

## 다음 단계

1. JS read-only adapter 구현
2. 합성 예시 fixture 변환 테스트
3. 프로토타입에 JSON load 모드 추가
4. 실제 ANE 질문 패키지 1개로 검증
