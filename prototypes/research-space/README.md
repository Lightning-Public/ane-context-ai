# Research Space v0.2 Prototype

ANE Context AI의 실제 Context Package를 사람이 탐색할 수 있는 Research Space UI 실험이다.

## 실행

이 버전은 `examples/context-package.example.json`을 `fetch()`로 읽기 때문에 `file://`로 직접 열지 않고 저장소 루트에서 작은 HTTP 서버를 실행한다.

```bash
python -m http.server 8000
```

브라우저에서 다음 경로를 연다.

```text
http://localhost:8000/prototypes/research-space/
```

## 현재 클릭 흐름

1. 시작 화면에서 `예시 Context Package 불러오기` 클릭
2. `examples/context-package.example.json` 로드
3. Context Package v0.1.0을 read-only adapter로 그래프 변환
4. `Canvas 열기` 클릭
5. question / claim / evidence / uncertainty / provenance / review 노드 확인
6. 노드를 선택해 Inspector에서 원본 데이터 확인
7. supports / challenges / grounded_in 등의 edge 관계 확인
8. `현재 패키지를 문서로 보기`에서 간단한 Manuscript projection 확인

## Context Package adapter

`context-package-adapter.mjs`는 `schemas/context-package.schema.json` v0.1.0 패키지를 Research Space 그래프 모델로 투영한다.

현재 지원:

- question → question node
- evidence → evidence node
- claims → claim node
- supporting/challenging evidence → supports/challenges edge
- debates / positions / open questions
- uncertainties와 grounded evidence
- bibliography → source node
- retrieval / review provenance

변환은 read-only이며 원본 패키지를 수정하지 않는다.

## Loader / layout

`context-package-loader.mjs`는 두 역할만 가진다.

1. JSON 파일을 안전하게 로드하고 adapter에 전달
2. 그래프 노드를 타입별 열(column)에 배치할 최소 Canvas 좌표 생성

레이아웃은 시각적 검증을 위한 임시 구현이며 의미 모델의 일부가 아니다.

## 테스트

```bash
node prototypes/research-space/context-package-adapter.test.mjs
node prototypes/research-space/context-package-loader.test.mjs
```

테스트 범위:

- Context Package → graph 변환
- evidence → claim `supports` 관계 보존
- uncertainty 보존
- 지원하지 않는 schema version 거부
- loader의 HTTP 실패 처리
- 모든 노드에 Canvas 좌표 생성

원격 GitHub 편집 세션에서는 Node 런타임 테스트를 직접 실행하지 못하므로, 병합 전 로컬 또는 CI에서 위 두 명령을 실행해야 한다.

## 실제 데이터 연결 상태

현재 Canvas는 더 이상 HTML에 박힌 합성 노드를 사용하지 않는다.

```text
examples/context-package.example.json
        ↓ fetch
context-package-loader.mjs
        ↓
context-package-adapter.mjs
        ↓
Research Space graph
        ↓
Canvas / Inspector / Manuscript projection
```

## 검증 목적

- Context Package의 학술적 층위를 UI에서도 잃지 않는가?
- 채팅 로그보다 노드/관계 구조가 연구 상태를 이해하기 쉬운가?
- Evidence / Claim / Uncertainty의 차이가 시각적으로 구분되는가?
- 각 노드에서 원본 Context Package 데이터를 역추적할 수 있는가?
- 같은 Context Package에서 Canvas와 문서 View를 함께 만들 수 있는가?

## 현재 제한

- 실제 ORACC/CDLI live data와 연결하지 않는다.
- adapter와 Canvas는 read-only다.
- edge routing과 자동 레이아웃은 단순한 임시 구현이다.
- 실제 LLM 호출이 없다.
- 3D Canvas는 구현하지 않는다.
- bibliography와 claim 사이에는 현 스키마상 직접 참조 ID가 없어 자동 연결하지 않는다.

## 다음 연결점

1. Evidence / Claim / Debate / Uncertainty를 더 명확한 시각 레이어로 분리
2. 실제 ANE 연구 질문의 Context Package 1개 생성
3. 해당 패키지 end-to-end 렌더링 검증
4. 사용자 승인 이벤트 모델
5. 수정 사항을 원본에 직접 쓰지 않고 Context Package delta로 기록
