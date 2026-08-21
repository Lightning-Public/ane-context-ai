# R002 — 문자는 왜 탄생했는가?

## 연구 질문
초기 메소포타미아에서 기록과 문자는 어떤 사회적·행정적 문제를 해결하며 발전했는가?

## 목적
이 연구는 ANE Context AI의 첫 학습-연구 통합 파일럿이다. ANE 101 Module 3의 초보자 질문을 실제 1차 사료 검색과 Context Package 생성으로 연결한다.

## 초기 범위
- 지역: 남부 메소포타미아, 특히 Uruk 관련 자료
- 시기: 기원전 4천년기 후반 중심
- 자료 유형: 초기 행정 점토판, 수·기호 체계, 관련 고고학 맥락
- 주요 데이터 후보: ORACC의 공개 프로젝트/PCSL 계열 자료, CDLI의 유물 메타데이터와 식별자

## 현재 상태

2026-08-21 첫 live verification에서 Source Pack v0.1의 CDLI P-number 24건이 모두 현재 API에서 해석되었다.

- 시도: 24
- resolved: 24
- 오류: 0
- 후보 period와 명시적으로 일치: 23
- period 누락: 1
- provenience 누락: 3
- provenience가 uncertain: 6

상세 실행 기록: [live-verification-2026-08-21.md](live-verification-2026-08-21.md)

첫 Context Package는 다음 세 자료를 검토 대상으로 삼는다.

- `P002718`: CDLI 현재 장르 `Administrative`, 그러나 `LGE 5 / Geography 5` 연계 검토 필요
- `P000014`: `Lexical`, Archaic Pigs witness
- `P000021`: `Lexical > Vocabularies`, Archaic Vocabulary witness

Context Package: `examples/r002-origin-of-writing.context-package.json`

2026-08-21 AI-assisted source audit 결과 review 상태는 **`needs_revision`**이다.

- 정확한 전사 행과 `#`, `?`, `[...]`, `X` 표지를 복원했다.
- CDLI metadata와 transliteration revision history를 기록했다.
- Damerow 2006의 행정·lexical list 해석을 secondary evidence로 추가했다.
- `P002718`의 장르·기능 분류 충돌을 발견했다.
- ATU 3 도판의 독립 collation과 Assyriologist 검토가 남아 있으므로 `source_checked`로 승격하지 않았다.

검토 기록: [reviews/2026-08-21-ai-source-audit.md](reviews/2026-08-21-ai-source-audit.md)

## v0.1 Source Pack
처음부터 대량 코퍼스를 수집하지 않는다. 20~50건의 소규모 고품질 자료 묶음을 만든다.

현재 첫 working set으로 Uruk III 후보 24건을 고정했다.

- 사람용 설명: [source-pack-v0.1.md](source-pack-v0.1.md)
- 기계 판독 manifest: `data/manifests/r002-source-pack-v0.1.json`
- CDLI 검증기: [cdli-verifier.md](cdli-verifier.md)
- live verification: [live-verification-2026-08-21.md](live-verification-2026-08-21.md)
- CDLI 재사용 경계: `data/manifests/cdli-terms-2026-06-13.json`
- Damerow 2006 source manifest: `data/manifests/damerow-2006-cdlj.json`
- source audit: [reviews/2026-08-21-ai-source-audit.md](reviews/2026-08-21-ai-source-audit.md)
- 다음 개발 체크포인트: [next-development.md](next-development.md)

24건은 여전히 `candidate`다. CDLI live metadata 조회가 성공해도 verifier는 자동으로 역사적 근거 상태로 승격하지 않는다. 선택한 세 자료도 `metadata_checked_needs_expert_review` 주석만 추가했으며 `verified`로 올리지 않았다.

권장 전체 구성:
- 초기 점토판 10~20건
- 대표 숫자·기호 또는 표기 사례 5~10건
- 고고학·연대 Context 5건 내외
- 현대 학술 해설·개론 5~10건

## 필수 메타데이터
각 자료는 가능한 범위에서 다음을 유지한다.

- source_id
- object_id / text_id
- source_database
- period / date_range / chronology_system
- provenience / place
- genre
- language / script stage
- transliteration 또는 sign data
- scholarly translation/interpretation
- bibliography
- license / redistribution status
- certainty / editorial status

## 연구 가설을 다루는 방식
`도시의 행정 복잡성이 문자 발생을 촉진했다`는 문장은 출발 가설이지 자동 결론이 아니다.

Context Package에서 다음을 분리한다.
1. 실제 자료가 직접 보여주는 기록 행위
2. 현재 catalogue가 부여한 장르
3. 판본과 전사 책임
4. 기록 기능에 대한 현대 학계의 해석
5. 지역·시기별 차이
6. 대안 설명
7. 현재 자료로 판단하기 어려운 부분

Damerow의 해석은 대다수 proto-cuneiform 자료를 bookkeeping과 행정 맥락에 연결하면서도 lexical lists를 학교 훈련과 지식 조직의 일부로 본다. 따라서 “행정 대 lexical”을 단순 대립으로 처리하지 않는다.

## 평가 질문
- 가장 초기 기록은 무엇을 세고 분류했는가?
- 기록의 대상은 도시 경제의 어떤 활동과 연결되는가?
- 수 체계와 표기 체계는 어떤 관계를 보이는가?
- 문자 발생을 단일한 '발명 순간'으로 설명하는 것이 적절한가?
- lexical list는 행정 기록의 반대 사례인가, 행정적 표기 체계의 확장인가?
- 행정 기록에서 언어적 문장 기록으로의 변화는 어떻게 추적할 수 있는가?

## 완료 조건
- Source Pack의 모든 항목이 원 출처와 안정 식별자로 되돌아갈 수 있다.
- 핵심 주장에는 실제 자료 또는 명시적인 현대 연구 근거가 연결된다.
- 학습용 설명과 연구용 증거 레이어가 분리된다.
- 초보자가 같은 질문으로 첫 Context Package를 생성할 수 있다.
- 검색 결과와 인용 범위를 재현할 수 있다.
- Context Package의 역사적 해석이 관련 분야 사람 검토를 받는다.
- AI-assisted audit만으로 `source_checked` 또는 `verified` 상태를 부여하지 않는다.

## 다음 작업

1. Issue #5에서 `P002718`의 `Administrative` 대 `LGE 5 / Geography 5` 관계를 해결한다.
2. Issue #6에서 ATU 3 pl. 36, 78, 80을 line-by-line collate한다.
3. Issue #7에서 필요하면 더 명확한 administrative comparator를 선정한다.
4. Issue #8에서 사람 Assyriological review와 상태 승격 절차를 정의한다.
5. Issue #4에서 Uruk IV 자료와 대표 PCSL sign을 포함하는 Source Pack v0.2를 만든다.
6. source review가 끝난 Context Package를 초보자 학습 화면에 연결한다.

## 다음 연구와의 연결
R002 완료 후 R001 `신아시리아 제국은 어떻게 거대한 영토를 통치했는가?`로 확장하여 왕실 비문, 편지, 조약, 행정자료처럼 서로 다른 장르의 교차 검색을 시험한다.
