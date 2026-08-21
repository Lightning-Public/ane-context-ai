# R002 다음 개발 체크포인트

현재 개발 단위에서 CDLI artifact verifier, batch manifest verifier, CLI, 단위 테스트, CI workflow를 추가했다.

## 완료된 기반

- `P-number -> /artifacts/{numeric}.json` 조회 규칙
- 외부 의존성 없는 Python 표준 라이브러리 HTTP client
- period / provenience / genre / collection / museum number / publication 정규화
- inscription 존재 여부 기록
- retrieval timestamp와 resolved/error 집계
- candidate 상태 자동 승격 금지
- raw CDLI payload 미보존
- `ane-context verify-cdli` CLI
- 네트워크 없는 unit tests

## 다음 체크포인트: live verification

1. Source Pack v0.1의 24개 P-number를 실제 CDLI에 조회한다.
2. 반환되는 실제 JSON schema를 기준으로 alias/관계 필드를 보강한다.
3. 각 후보를 `resolved`, `metadata-review`, `error`로 분류한다.
4. period 불일치 또는 누락을 사람 검토 대상으로 분리한다.
5. metadata/text/image 권리 상태를 별도 기록한다.
6. 승인 조건을 충족한 artifact만 `verified`로 승격한다.

## 그 다음: 첫 Context Package

verified artifact 중 교육적으로 설명 가능한 1~3건을 선정해 다음 질문에 대한 첫 실제 Context Package를 만든다.

> 초기 메소포타미아에서 기록과 문자는 어떤 사회적·행정적 문제를 해결하며 발전했는가?

이 단계에서는 한 점토판이 직접 보여주는 것과, 문자 기원의 일반 이론을 엄격히 분리한다.
