# Research Space v0.1 Prototype

ANE Context AI의 Context Package를 사람이 탐색하고 수정할 수 있는 Research Space UI 실험이다.

## 실행

별도 빌드 없이 `index.html`을 브라우저에서 연다.

## 현재 클릭 흐름

1. 새 연구 화면에서 제목·질문 입력
2. `AI가 연구 구조 제안하기` 클릭
3. Research Canvas로 이동
4. 질문/가설/근거/실험/반론 노드 선택
5. Inspector에서 선택 노드 확인
6. AI 반론 제안 승인/거절
7. `현재 구조를 문서로 보기` 클릭
8. Manuscript View에서 현재 연구 구조의 문서 투영 확인

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

테스트:

```bash
node prototypes/research-space/context-package-adapter.test.mjs
```

상세 매핑 원칙은 `docs/product/research-space-context-package-mapping.md`를 참고한다.

## 검증 목적

이 프로토타입은 그래픽 완성도가 아니라 다음 가설을 검증한다.

- 채팅 로그보다 노드/관계 구조가 연구 상태를 이해하기 쉬운가?
- AI의 제안과 사용자의 승인을 분리하는 UX가 자연스러운가?
- 반론과 미해결점을 문서 생성 전에 보존할 수 있는가?
- 동일한 Research Space를 여러 문서 View로 투영할 수 있는가?

## 현재 제한

- Canvas 화면은 아직 합성 UI 데이터를 사용한다.
- 실제 ORACC/CDLI 데이터와 연결하지 않는다.
- adapter는 read-only이며 UI에서 Context Package를 수정하지 않는다.
- 실제 LLM 호출이 없다.
- 3D Canvas는 구현하지 않는다.

## 다음 연결점

다음 단계는 adapter 출력 그래프를 실제 Canvas에 주입하는 것이다.

권장 순서:

1. `examples/context-package.example.json` 로드 → Canvas 렌더링
2. Evidence / Interpretation / Debate / Uncertainty 시각적 분리
3. 사용자 승인 이벤트 모델
4. 수정된 Research Space → 검토용 Context Package delta
5. 실제 ANE 연구 질문 1개를 end-to-end로 실행
