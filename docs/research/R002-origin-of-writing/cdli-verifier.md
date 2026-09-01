# R002 CDLI verifier

`r002-source-pack-v0.1.json`의 후보 P-number를 현재 CDLI 메타데이터와 대조하기 위한 최소 검증기다.

## 목적

- P-number가 현재 CDLI artifact API에서 해소되는지 확인한다.
- period, provenience, genre, collection, museum number, publication 등 확인 가능한 메타데이터를 보존한다.
- 조회 시각과 CDLI URL을 기록한다.
- 불확실하거나 누락된 값을 추정해서 채우지 않는다.
- 원격 raw JSON, 이미지, 전사, 번역을 그대로 저장하지 않는다.

CDLI의 공식 REST API 문서는 artifact metadata에 JSON export를 지원하며 `/artifacts/*` 경로를 제공한다. verifier는 `P006427`을 numeric artifact id `6427`로 변환하여 `/artifacts/6427.json`을 조회한다.

## 실행

```bash
PYTHONPATH=src python -m ane_context_ai verify-cdli \
  data/manifests/r002-source-pack-v0.1.json \
  --output data/processed/r002-source-pack-v0.1.verified.json
```

처음 한 건만 확인하려면:

```bash
PYTHONPATH=src python -m ane_context_ai verify-cdli \
  data/manifests/r002-source-pack-v0.1.json \
  --output /tmp/r002-check.json \
  --limit 1
```

## 결과 상태

- `candidate`: 원 Source Pack의 상태. verifier가 자동으로 바꾸지 않는다.
- `verification.status=resolved`: CDLI JSON endpoint가 응답했고 정규화된 메타데이터를 얻었다.
- `verification.status=error`: HTTP, JSON, P-number 등의 오류로 검증하지 못했다.
- `period_matches_candidate`: 후보의 period와 CDLI 응답 period가 모두 있을 때만 비교한다. 하나라도 없으면 `null`이다.
- `missing_fields`: `period`, `provenience`, `genre` 중 현재 응답에서 찾지 못한 필드를 명시한다.

`resolved`는 곧바로 역사적 근거로 승인되었다는 뜻이 아니다. 권리 확인, 메타데이터 검토, source disagreement 검토 후 별도의 승인 절차에서 `verified`로 승격한다.

## 저장 정책

verifier 결과에는 다음만 저장한다.

- P-number
- 안정 URL과 API URL
- 정규화한 메타데이터
- 응답의 top-level field 이름
- 검증 시각과 상태

CDLI raw payload 전체는 저장하지 않는다. 향후 API 응답에 전사나 다른 권리 제한 콘텐츠가 포함되어도 Source Pack에 우발적으로 복제하지 않기 위한 조치다.

## 테스트

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

테스트는 외부 네트워크를 사용하지 않고 injectable transport와 합성 CDLI 응답으로 URL 생성, 중첩 메타데이터 정규화, 후보 상태 보존, batch timestamp/count를 확인한다.

## 다음 단계

1. 실제 CDLI에서 24개 후보를 실행 검증한다.
2. 응답 schema와 현재 정규화 alias가 맞지 않는 필드를 보강한다.
3. period 불일치와 누락 필드를 사람이 검토한다.
4. 권리 상태를 별도 필드로 기록한다.
5. 승인된 항목만 `verified`로 승격한다.
6. verified artifact 1~3건으로 첫 R002 Context Package를 만든다.
