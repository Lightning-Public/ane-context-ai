# Research Space v0.1

## 한 줄 정의

Research Space는 사용자의 질문·가설·근거·반론·자료를 구조화된 연구 공간에 저장하고, AI가 그 공간을 탐색·보강하며, 필요할 때 논문·보고서·설명문 형태로 투영하는 ANE Context AI의 연구 인터페이스다.

## ANE Context AI와의 관계

이 인터페이스는 별도 제품이 아니라 기존 Context Package 흐름의 시각적·상호작용적 표현이다.

```text
Question
  → Context Package
  → Evidence / Interpretation / Debate / Uncertainty
  → Research Space
  → Manuscript / Report / Explanation
```

기존 프로젝트 원칙을 그대로 따른다.

- 출처 우선
- 층위 분리
- 불확실성 보존
- 재현 가능성
- 인간 검토

## v0.1 검증 목표

> 사용자가 채팅 로그가 아니라 연구 구조를 남기면서 사고를 확장할 수 있는가?

초기 MVP에서는 실제 3D 그래픽보다 다음 흐름을 우선한다.

1. 질문 생성
2. AI가 초기 연구 구조 제안
3. 사용자가 노드 승인·수정·삭제
4. 근거와 출처 연결
5. 반론 생성
6. 가설 상태 변경
7. 현재 연구 구조를 문서로 투영

## 핵심 노드

- Question
- Concept
- Claim
- Hypothesis
- Evidence
- Source
- Counterargument
- Experiment
- Insight

각 노드는 최소한 다음 상태를 가진다.

- proposed
- accepted
- rejected
- needs-evidence
- verified

## 핵심 관계

- supports
- contradicts
- derives_from
- answers
- explores
- requires
- refines
- alternative_to
- caused_by
- related_to

## 화면 구조

### 1. New Research

입력:

- 프로젝트 제목
- 시작 질문
- 연구 목적
- 선택: 대상 독자 / 결과 형식

CTA:

`AI가 연구 구조 제안하기`

### 2. Research Canvas

중앙 그래프에서 질문, 가설, 근거, 반론, 실험, 출처를 연결한다.

초기 버전은 2D를 기본으로 한다. 3D는 정보 모델과 작업 흐름이 검증된 뒤 Visualization 모드로 확장한다.

### 3. Inspector + AI Suggestions

선택 노드의 다음 정보를 확인한다.

- Type
- Title
- Content
- Summary
- Status
- Confidence
- Tags
- Source
- Related Nodes
- History

AI 액션:

- 근거 찾기
- 반론 생성
- 더 깊게 탐색
- 단순화
- 연결 후보 찾기

AI가 만든 핵심 노드는 기본적으로 `proposed` 상태이며 사용자가 Accept / Reject / Edit 한다.

### 4. Manuscript View

Research Space를 다음 형식으로 투영한다.

- 논문 초안
- 조사 보고서
- 쉬운 설명
- 발표 개요
- 반론 중심 글

문서의 각 문단은 사용된 Claim / Evidence / Source로 역추적 가능해야 한다.

## 승인 정책

AI가 자동으로 수행 가능:

- 관계 후보 추천
- 관련 노드 추천
- 요약
- 태그
- Source 메타데이터 정리
- 중복 후보 탐지

사용자 승인 필요:

- Claim / Hypothesis 채택
- Counterargument 채택
- 기존 내용 변경
- Branch Merge
- 최종 문서 반영

## Branch / Timeline

가설이나 주장 어느 지점에서든 대안 Branch를 만들 수 있다. 서로 다른 가설을 독립적으로 탐색하고, 수렴 시 새로운 Insight 또는 Hypothesis로 Merge한다.

Timeline은 단순 활동 로그가 아니라 연구 사고가 어떻게 바뀌었는지를 보존한다.

예:

```text
Hypothesis A 0.72
  → Evidence 추가
  → Counterargument 추가
  → Confidence 0.48
  → rejected
```

## 최소 데이터 모델

```json
{
  "node": {
    "id": "node_001",
    "type": "hypothesis",
    "title": "가설 제목",
    "content": "...",
    "status": "needs-evidence",
    "confidence": 0.62,
    "source_ids": []
  },
  "edge": {
    "from": "node_002",
    "to": "node_001",
    "relation": "supports",
    "confidence": 0.88
  }
}
```

향후에는 기존 Context Package 스키마와 직접 매핑한다.

## v0.1 비범위

- WebGL 기반 3D Canvas
- 다중 사용자 실시간 협업
- 완전 자율 연구 Agent
- 대규모 자동 논문 검색 파이프라인
- 연구 품질 자동 판정

## 프로토타입 성공 기준

1. 채팅보다 연구 구조를 이해하기 쉬운가?
2. 이전 사고로 돌아가기 쉬운가?
3. AI가 왜 특정 결론을 제안했는지 추적 가능한가?
4. 반론과 대안이 사라지지 않는가?
5. 같은 연구 공간에서 여러 형태의 글을 만들 수 있는가?

핵심 원칙:

> 3D를 보여주는 제품이 아니라, 사고가 여러 방향으로 존재할 수 있도록 만드는 제품을 먼저 만든다.
