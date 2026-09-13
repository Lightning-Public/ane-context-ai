# Research Space 실제 ANE E2E 검증

## 목적

Research Space가 단순 합성 예시가 아니라 실제 고대근동 연구 질문에서 다음 층위를 잃지 않고 표현할 수 있는지 검증한다.

- Question
- Evidence
- Claim
- Debate
- Position
- Open Question
- Uncertainty
- Bibliography
- Retrieval / Review provenance

## 검증 질문

> 후기 우루크기의 초기 문자는 주로 행정·경제 기록을 위해 사용되었는가?

이 질문은 초기 설형문자의 행정적 기능에 대한 강한 근거와, 그 근거를 문자의 단일 기원·단일 기능으로 과도하게 일반화하지 말아야 한다는 해석적 경계를 동시에 포함하기 때문에 Research Space 검증에 적합하다.

## 패키지

`examples/context-package.uruk-writing.json`

상태:

- `review.status`: `source_checked`
- expert-reviewed 아님
- UI end-to-end 검증용 최소 연구 패키지

사용한 공개 참고자료:

- The Metropolitan Museum of Art, *The Origins of Writing*
- The Metropolitan Museum of Art, early administrative account concerning malt and barley groats
- British Museum, *How to write cuneiform*

패키지는 각 자료의 stable URL, attribution, retrieval metadata를 보존한다.

## 의도적으로 보존한 논쟁

### Position A

도시화와 함께 증가한 행정·경제 관리 수요가 초기 문자 발달의 핵심 동인이었다.

### Position B

현존 점토 행정문서의 높은 비중만으로 문자의 전체 기원과 초기 기능을 단일 원인으로 환원해서는 안 된다.

두 position은 별도 노드로 유지하며 하나를 자동으로 정답 처리하지 않는다.

## 불확실성

패키지는 최소 다음 불확실성을 보존한다.

1. `coverage` — 점토판 중심 생존 자료가 전체 기록 문화를 대표하는지 불확실
2. `interpretation` — 행정 용례의 비중과 '발명의 주된 원인'은 같은 명제가 아님
3. `identity` — 가장 이른 원시 설형문자의 언어 귀속 문제

이 값들은 하나의 숫자 confidence로 합치지 않는다.

## E2E 실행

저장소 루트에서:

```bash
python -m http.server 8000
```

그 다음:

```text
http://localhost:8000/prototypes/research-space/ane-e2e.html
```

데이터 흐름:

```text
examples/context-package.uruk-writing.json
        ↓
context-package-loader.mjs
        ↓
context-package-adapter.mjs
        ↓
Research Space graph
        ↓
ANE E2E Canvas / Inspector
```

## 회귀 테스트

```bash
node prototypes/research-space/ane-e2e.test.mjs
```

검증 항목:

- Debate node 존재
- Position node 2개 이상
- Uncertainty node 2개 이상
- Evidence → Claim supports edge
- Debate → Position has_position edge
- Position → Evidence supported_by edge
- Debate → Question opens edge
- Uncertainty → Evidence grounded_in edge

## 완료 조건

Research Space가 실제 질문에서 다음을 동시에 보여주면 이 단계는 성공이다.

1. 행정 중심 설명을 강한 Claim으로 표현
2. 반대/제한 해석을 Debate Position으로 별도 보존
3. 자료 편향과 해석적 한계를 Uncertainty로 보존
4. 각 노드에서 원본 Context Package 데이터 역추적
5. 어느 하나의 Position도 UI가 자동으로 '최종 정답'으로 승격하지 않음
