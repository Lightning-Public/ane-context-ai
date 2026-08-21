# 첫 초보자용 Context Package 화면

## 목표

완전 초보자가 “문자는 왜 탄생했는가?”라는 질문을 읽으면서 다음 차이를 스스로 식별하도록 한다.

1. 유물·판본이 직접 제공하는 정보
2. 여러 자료를 비교해 도출한 제한적 결론
3. 현대 학자의 해석
4. AI가 제안할 수 있는 가설
5. 아직 해결되지 않은 판독·연대·표본·분류 문제

## 구조

```text
Context Package JSON
        ↓
provenance-preserving Learning View Model
        ↓
beginner-facing static screen
```

`src/ane_context_ai/learning_view.py`는 연구 객체의 source ID, locator, claim status, review state, uncertainty marker를 잃지 않고 화면 단위로 그룹화한다. 브라우저 프로토타입도 같은 규칙을 적용한다.

## 화면 정보 구조

- 질문과 현재 검토 상태
- Uruk 개념 지도와 Uruk IV → III 연대표
- P-number별 유물 신원·전사 카드
- 직접 증언 / 파생 결론 / 학술 해석 lane
- 논쟁의 서로 다른 입장
- 불확실성과 차단 finding
- 검색·manifest·review provenance
- 다음 연구 질문

## 연구 안전장치

- `needs_revision`을 상단과 provenance 영역에 동시에 노출한다.
- 모든 artifact 카드는 `verified 아님`을 표시한다.
- CDLI 이미지와 line art를 복제하지 않는다.
- 전사의 `#`, `?`, `[...]`, `X`를 그대로 렌더링한다.
- source link와 locator를 모든 evidence block에 제공한다.
- Uruk III 세 자료가 최초 문자 발생을 직접 증명하지 못한다는 한계를 연대표와 claim lane에서 반복 확인한다.

## 실행

```bash
python -m http.server 8000
```

```text
http://localhost:8000/web/r002/
```

## View Model 생성

```bash
PYTHONPATH=src python -m ane_context_ai build-learning-view \
  examples/r002-origin-of-writing.context-package.json \
  --output /tmp/r002-learning-view.json
```

## 완료 조건

- 데스크톱과 모바일에서 정보 순서가 유지된다.
- 사용자가 fact / derived / scholarship / uncertainty를 구분할 수 있다.
- 검토 상태를 개발자 JSON을 열지 않고 확인할 수 있다.
- 제한 자료 이미지를 포함하지 않고도 학습 흐름이 성립한다.
- Python View Model 테스트와 정적 화면 계약 테스트가 CI에서 통과한다.
