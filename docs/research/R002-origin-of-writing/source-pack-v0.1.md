# R002 Source Pack v0.1 — Uruk III working set

## 목적
이 문서는 `R002 — 문자는 왜 탄생했는가?` 연구를 위한 첫 재현 가능 작업 샘플을 고정한다. 이 단계의 목적은 대표성을 완성하는 것이 아니라, **CDLI 안정 식별자(P-number)를 유지한 소규모 코퍼스가 Context Package 파이프라인을 끝까지 통과하는지 검증**하는 것이다.

## 선정 원칙

- 원 출처의 기준 식별자는 CDLI P-number로 둔다.
- `Nino-cunei/uruk` Text-Fabric 1.0 코퍼스는 **선정·교차검증 보조 자료**로만 사용한다. 이 코퍼스는 CDLI에서 파생된 Uruk IV–III 자료라고 명시한다.
- `catalogId.tf`와 `period.tf`는 동일 Text-Fabric tablet node 순서에 대응한다. 첫 24개 P-number는 해당 period feature의 초기 연속 구간과 대응하며 `uruk-iii`로 기록한다.
- 이미지, 전체 전사, 번역을 이 저장소에 복제하지 않는다. 우선 식별자와 메타데이터·검증 상태만 관리한다.
- 각 P-number의 최신 메타데이터는 이후 CDLI live API/검색으로 다시 검증한다.

## 출처

- CDLI: https://cdli.earth/
- Nino-cunei Uruk corpus: https://github.com/Nino-cunei/uruk
- Text-Fabric catalog IDs: https://github.com/Nino-cunei/uruk/blob/master/tf/1.0/catalogId.tf
- Text-Fabric period feature: https://github.com/Nino-cunei/uruk/blob/master/tf/1.0/period.tf

## Working set A — Uruk III, 24 objects

| # | CDLI ID | Phase | 상태 |
|---:|---|---|---|
| 1 | P006427 | Uruk III | candidate |
| 2 | P006428 | Uruk III | candidate |
| 3 | P448701 | Uruk III | candidate |
| 4 | P448702 | Uruk III | candidate |
| 5 | P448703 | Uruk III | candidate |
| 6 | P471695 | Uruk III | candidate |
| 7 | P482082 | Uruk III | candidate |
| 8 | P482083 | Uruk III | candidate |
| 9 | P499393 | Uruk III | candidate |
| 10 | P504412 | Uruk III | candidate |
| 11 | P504413 | Uruk III | candidate |
| 12 | P006438 | Uruk III | candidate |
| 13 | P000014 | Uruk III | candidate |
| 14 | P000456 | Uruk III | candidate |
| 15 | P002718 | Uruk III | candidate |
| 16 | P000021 | Uruk III | candidate |
| 17 | P000023 | Uruk III | candidate |
| 18 | P000025 | Uruk III | candidate |
| 19 | P000167 | Uruk III | candidate |
| 20 | P000453 | Uruk III | candidate |
| 21 | P000434 | Uruk III | candidate |
| 22 | P000481 | Uruk III | candidate |
| 23 | P000488 | Uruk III | candidate |
| 24 | P000628 | Uruk III | candidate |

## 이 샘플로 검증할 것

1. P-number → 최신 CDLI object metadata 조회가 가능한가?
2. 출토지, 시기, 장르, 소장처, 출판 정보가 손실 없이 정규화되는가?
3. 원문/전사 데이터가 허용되는 경우, line/sign 단위 식별을 보존할 수 있는가?
4. 동일 object를 ORACC/PCSL의 sign·text 정보와 연결할 수 있는가?
5. AI가 `증거`, `현대 해석`, `추론`을 분리한 Context Package를 생성하는가?

## 대표성에 대한 제한

이 24건은 **대표 표본이 아니라 파이프라인 검증용 working set**이다. 연속된 코퍼스 인덱스에서 재현 가능하게 선택했기 때문에 장르·출토 맥락·수 체계가 편향될 수 있다. 따라서 이 자료만으로 `문자의 탄생 원인`에 대한 역사적 결론을 내리지 않는다.

## Source Pack v0.2로 확장할 기준

Working set A를 정상 처리한 뒤 다음 층화를 추가한다.

- Uruk IV 자료 10건 이상
- 수치/계량 기호가 두드러진 자료
- 물자·배급·노동·가축 등 서로 다른 행정 범주
- lexical/list 계열과 administrative 계열의 비교
- 출토 맥락이 비교적 명확한 자료 우선
- PCSL에서 빈도와 분포를 확인할 수 있는 대표 sign 사례 5~10개

## 승격 규칙

각 candidate는 다음 조건을 만족하면 `verified`로 승격한다.

- CDLI에서 P-number가 현재 유효함
- period/provenience/genre를 최신 원 출처로 확인함
- 사용하려는 이미지·전사·번역의 권리 상태를 기록함
- 교육 화면에서 사용할 경우 초보자 설명과 연구자용 원자료 링크를 분리함

이 문서는 Source Pack의 시작점이며, 실제 연구 근거는 `verified` 상태의 항목만 사용한다.
