# 아키텍처 초안

## 설계 목표

- 출처와 식별자를 잃지 않는 수집·정규화
- 원문, 전사, 번역, 해석을 분리한 검색
- RAG와 Knowledge Graph의 상호 보완
- 작은 코퍼스에서 검증한 뒤 점진적으로 확장
- 데이터 조건 변경 시 해당 레코드를 추적·삭제할 수 있는 계보

## 전체 흐름

```text
공식 소스
  │
  ├─ 소스 어댑터 ── 권리/속도 제한 사전 점검
  │
  ├─ immutable raw snapshot + checksum (로컬/승인된 저장소)
  │
  ├─ 정규화 ── provenance ledger ── 식별자 교차표
  │
  ├─ 텍스트 저장소 ── lexical index ── vector index
  │
  └─ claim graph ── entities + sourced relationships
                         │
질문 ── query planner ───┼── retrieval + reranking
                         │
                  evidence bundle
                         │
              Context Package composer
                         │
               citation/policy validator
```

## 구성 요소

### 1. Source Registry

소스별 공식 URL, 허용 범위, 라이선스 근거, 인용 형식, 획득 방법, 속도 제한, 마지막 확인일을 관리한다. 허용 상태가 `unknown`이면 어댑터는 기본적으로 수집을 중단한다.

### 2. Source Adapters

ORACC, CDLI, eBL, TLA를 공통 형식으로 억지로 평탄화하지 않는다. 각 어댑터는 원 소스 의미를 보존한 중간 레코드를 만들고 다음을 공통 봉투(envelope)에 넣는다.

- 원 식별자와 URL
- 원 응답/아카이브 체크섬
- 획득 시각과 쿼리
- 자료 유형과 권리 매니페스트
- 파서 버전과 경고

### 3. Normalized Research Model

핵심 엔터티는 다음과 같다.

- `Artifact`: 물리적 유물
- `TextWitness`: 특정 유물에 기록된 텍스트 증언
- `Composition`: 여러 증언으로 전하는 추상적 작품
- `Passage` / `Token`: 행·절·단어 단위
- `Person`, `Place`, `Polity`, `Deity`
- `Period` / `ChronologyAssertion`
- `Language`, `Genre`
- `Edition`, `Translation`, `Publication`
- `Claim`, `Evidence`, `Uncertainty`

소스 필드는 보존하고, 정규화 값은 별도 파생 필드로 만든다. 예를 들어 원 연대 문자열을 덮어쓰지 않고 `normalized_interval`, `chronology_system`, `normalizer_version`을 추가한다.

### 4. Retrieval Layer

초기 순서는 단순하고 측정 가능하게 유지한다.

1. 메타데이터 필터
2. BM25/형태소 기반 검색
3. 임베딩 검색
4. 판본·장르·소스 다양성 재정렬
5. 그래프 이웃 확장
6. 행 단위 인용 가능성 검사

전사, 정규화 전사, 번역, 설명을 서로 다른 필드로 인덱싱한다. 번역 임베딩만으로 원어의 의미를 대표하지 않는다.

### 5. Claim Graph

일반 지식 그래프의 단정적 삼중항 대신, 관계를 출처 있는 주장 노드로 모델링한다.

```text
(claim)-[:SUBJECT]->(entity)
(claim)-[:PREDICATE]->(relation type)
(claim)-[:OBJECT]->(entity/value)
(claim)-[:SUPPORTED_BY]->(evidence)
(claim)-[:CHALLENGED_BY]->(evidence)
```

이 구조는 서로 다른 연대안, 지명 동일시, 텍스트 복원을 동시에 보존한다.

### 6. Context Package Composer

검색 결과를 바로 자연어 답변으로 넘기지 않는다. 먼저 구조화된 evidence bundle을 만들고 주장마다 근거를 연결한다. 스키마 검증과 인용 검사를 통과한 후 요약문을 생성한다.

## 저장 기술 방향

MVP에서는 기술 선택보다 데이터 계약을 우선한다.

- 원본: 콘텐츠 주소형 파일 + SHA-256, Git 외부
- 정규화 테이블: Parquet/DuckDB로 시작 가능
- 키워드 검색: SQLite FTS 또는 OpenSearch 후보
- 벡터 검색: 로컬 벡터 확장 또는 전용 인덱스 후보
- 그래프: 관계형 claim tables로 시작하고 필요 시 그래프 DB 도입
- 메타데이터/계보: 관계형 저장소와 append-only acquisition log

그래프 DB를 초기에 필수로 두지 않는다. 질문 세트에서 다중 홉 탐색이 실제로 개선되는지 확인한 뒤 도입한다.

## 보안·운영 경계

- API 키와 세션 쿠키는 저장소에 넣지 않는다.
- 원격 텍스트를 프롬프트 명령으로 실행하지 않고 데이터로 취급한다.
- HTML/마크업은 안전하게 정규화하며 원문은 격리 저장한다.
- 외부 URL 가져오기는 허용 목록, 크기 제한, 콘텐츠 유형 검사를 적용한다.
- 사용자 입력 쿼리와 모델 출력으로 파일 경로나 원격 요청 대상을 직접 결정하지 않는다.
- 데이터 삭제 요청은 계보를 따라 원본, 인덱스, 파생 캐시에서 처리한다.

## 첫 수직 실험의 완료 산출물

1. ORACC 프로젝트 1개의 승인된 소스 매니페스트
2. 재실행 가능한 획득 및 체크섬 로그
3. 문헌/행/단어 식별자를 보존한 정규화 샘플
4. 질문 10개와 관련 구절 기준 세트
5. 키워드 기준선과 하이브리드 검색 비교
6. 스키마를 통과하는 Context Package 10개
7. 라이선스·인용·출처 완결성 검사 보고서
