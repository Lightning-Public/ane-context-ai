# R002 다음 개발 체크포인트

현재 개발 단위에서 CDLI artifact verifier, batch manifest verifier, CLI, 단위 테스트, CI workflow와 첫 live verification을 완료했다.

## 완료된 기반

- `P-number -> /artifacts/{numeric}.json` 조회 규칙
- CDLI 단일 artifact 응답의 길이 1 JSON 배열 처리
- 외부 의존성 없는 Python 표준 라이브러리 HTTP client
- period / provenience / genre / collection / museum number / publication 정규화
- inscription 존재 여부 기록
- retrieval timestamp와 resolved/error 집계
- candidate 상태 자동 승격 금지
- raw CDLI payload 미보존
- `ane-context verify-cdli` CLI
- 네트워크 없는 unit tests
- GitHub Actions unit test 및 live verification workflow

## 완료된 live verification

2026-08-21 실행에서 Source Pack v0.1의 24개 P-number가 모두 현재 CDLI API에서 해석되었다.

- attempted: 24
- resolved: 24
- errors: 0
- period 명시 일치: 23
- period 누락: 1
- provenience 누락: 3
- provenience uncertain: 6

상세 내용은 [live-verification-2026-08-21.md](live-verification-2026-08-21.md)를 따른다.

## 완료된 첫 Context Package 초안

다음 세 자료를 선택했다.

- `P002718`: Administrative
- `P000014`: Lexical
- `P000021`: Vocabularies

초안 위치:

- `examples/r002-origin-of-writing.context-package.json`

초안은 schema/semantic validator 테스트를 통과하지만 review 상태는 `unreviewed`다. 자료 식별과 역사적 해석의 검토 수준을 섞지 않는다.

## 다음 체크포인트: source review

1. 세 자료의 CDLI artifact metadata와 primary publication을 사람이 대조한다.
2. transliteration 책임 주체와 판본 이력을 확인한다.
3. Context Package의 각 claim을 `attested`, `derived`, `scholarly_interpretation`으로 재검토한다.
4. source-level 권리 manifest와 item-level 이미지·line art 권리를 구분한다.
5. 조건을 충족한 Context Package만 `source_checked`로 승격한다.

## 다음 체크포인트: Source Pack v0.2

1. Uruk IV 자료를 층화 표본으로 추가한다.
2. 대표 숫자·계량 기호와 PCSL sign 사례를 연결한다.
3. Uruk III 자료와 최초 기록 단계의 시간 차이를 명시한다.
4. 행정·lexical·vocabulary 장르의 선택 편향을 평가한다.
5. earliest writing에 관한 현대 연구 문헌을 secondary evidence 레이어로 추가한다.

## 학습 인터페이스 연결

첫 학습 화면에서는 다음 레이어를 분리한다.

```text
질문
  -> 지도와 연대표
  -> 실제 artifact
  -> transliteration
  -> 자료가 직접 보여 주는 것
  -> 현대 연구자의 해석
  -> 논쟁과 불확실성
  -> 다음 탐구 질문
```

이 단계에서는 한 점토판이 직접 보여주는 것과 문자 기원의 일반 이론을 엄격히 분리한다.
