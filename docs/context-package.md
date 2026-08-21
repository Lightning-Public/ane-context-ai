# Context Package 규격

Context Package는 자연어 답변이 아니라, 답변과 검토를 재생성할 수 있는 구조화된 연구 묶음이다. [JSON Schema](../schemas/context-package.schema.json)가 최소 기계 계약이며, 이 문서는 의미 규칙을 정의한다.

## 최상위 필드

| 필드 | 의미 |
|---|---|
| `id` | 패키지의 영구 내부 식별자 |
| `schema_version` | 데이터 계약 버전 |
| `question` | 원 질문, 정규화 질문, 범위 |
| `evidence` | 원 출처로 되돌아갈 수 있는 증거 단위 |
| `claims` | 증거·반증과 연결된 원자적 주장 |
| `debates` | 경쟁 해석과 각 입장의 근거 |
| `uncertainties` | 판독·연대·동일시·해석의 불확실성 |
| `bibliography` | 사용한 판본과 연구 문헌 |
| `retrieval` | 소스 스냅샷, 쿼리, 도구 버전 |
| `review` | 사람 검토 상태와 기록 |

## 질문 범위

질문에는 원문을 보존하고, 검색을 위한 정규화 문장을 별도로 둔다. `scope`는 다음을 표현할 수 있다.

- 시간 구간과 연대 체계
- 고대/현대 지명과 공간 범위
- 언어와 방언
- 장르와 자료 유형
- 포함·제외 기준

빈 범위는 “제한 없음”이 아니라 “아직 명시하지 않음”으로 해석한다.

## Evidence

증거는 인용 가능한 최소 단위다.

- `source`: ORACC/CDLI/eBL/TLA 또는 학술 출판물
- `source_record_id`: 원 시스템 식별자
- `stable_url`: 사람이 확인할 수 있는 URL
- `locator`: 행, 열, 면, 페이지, 섹션
- `layer`: artifact, image, transliteration, translation, edition, secondary
- `excerpt`: 라이선스가 허용하는 최소 인용 또는 로컬 참조
- `attribution`: 편집자·번역자·기관
- `license_manifest_id`: 데이터 거버넌스 매니페스트 연결

전사와 번역이 같은 화면에서 왔더라도 별도 evidence로 만들 수 있다. 번역에는 번역 책임 주체를 반드시 남긴다.

## Claims

주장은 다음을 가진다.

- `statement`: 한 가지 핵심 판단
- `status`: attested, derived, scholarly_interpretation, model_inference
- `supporting_evidence_ids`
- `challenging_evidence_ids`
- `confidence`: high, medium, low, unknown
- `reasoning`: 증거가 주장을 지지하는 방식의 짧은 설명

`model_inference`는 사람 검토 전에는 최종 요약의 단정문으로 승격할 수 없다.

## Debates

논쟁은 “학자 A 대 학자 B”의 이름 목록이 아니라 다음 구조를 갖는다.

- 논쟁의 정확한 쟁점
- 각 입장의 주장
- 각 입장이 사용하는 증거
- 반례와 방법론적 차이
- 현재 합의 수준을 판단한 출처
- 아직 필요한 증거

## Uncertainties

불확실성에는 대상, 종류, 설명, 가능한 값/범위, 근거, 해결에 필요한 검토를 기록한다. 서로 양립할 수 없는 연대나 동일시가 있다면 하나를 덮어쓰지 않는다.

## Retrieval Record

재현에 필요한 최소 정보는 다음과 같다.

- 실행 시각
- 소스 매니페스트 및 스냅샷 ID
- 원 쿼리와 생성된 하위 쿼리
- 필터와 상위 k
- 검색기, 임베딩, 재정렬기 버전
- 그래프 스냅샷
- 생성 모델과 프롬프트 템플릿 버전

민감한 인증정보나 내부 토큰은 기록하지 않는다.

## 검토 상태

- `unreviewed`: 자동 생성 또는 기계 변환만 완료
- `source_checked`: 인용 위치와 원 출처 확인
- `expert_reviewed`: 해당 분야 검토자가 내용 검토
- `needs_revision`: 오류 또는 중요한 누락 확인

검토는 패키지 전체의 영구 보증이 아니다. 소스나 스키마 버전이 바뀌면 재검토가 필요할 수 있다.
