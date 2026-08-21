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

첫 Context Package 초안은 다음 세 자료를 비교한다.

- `P002718`: Administrative
- `P000014`: Lexical
- `P000021`: Vocabularies

초안: `examples/r002-origin-of-writing.context-package.json`

현재 review 상태는 `unreviewed`다. 식별자와 현재 메타데이터가 해석되었다는 사실과, 역사적 주장이 검증되었다는 사실을 구분한다.

## v0.1 Source Pack
처음부터 대량 코퍼스를 수집하지 않는다. 20~50건의 소규모 고품질 자료 묶음을 만든다.

현재 첫 working set으로 Uruk III 후보 24건을 고정했다.

- 사람용 설명: [source-pack-v0.1.md](source-pack-v0.1.md)
- 기계 판독 manifest: `data/manifests/r002-source-pack-v0.1.json`
- CDLI 검증기: [cdli-verifier.md](cdli-verifier.md)
- live verification: [live-verification-2026-08-21.md](live-verification-2026-08-21.md)
- CDLI 재사용 경계: `data/manifests/cdli-terms-2026-06-13.json`
- 다음 개발 체크포인트: [next-development.md](next-development.md)

24건은 여전히 `candidate`다. CDLI live metadata 조회가 성공해도 verifier는 자동으로 역사적 근거 상태로 승격하지 않는다. 메타데이터·권리·불일치 검토 후 별도 승인된 항목만 `verified`가 된다.

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
2. 그 기록의 기능에 대한 현대 학계의 해석
3. 지역·시기별 차이
4. 대안 설명
5. 현재 자료로 판단하기 어려운 부분

첫 초안은 “행정 기록이 존재한다”와 “문자는 행정 때문에 발명되었다” 사이의 차이를 명시적으로 보존한다. Uruk III의 administrative, lexical, vocabulary 자료를 함께 비교하지만, 이 표본만으로 최초 발생의 단일 원인을 확정하지 않는다.

## 평가 질문
- 가장 초기 기록은 무엇을 세고 분류했는가?
- 기록의 대상은 도시 경제의 어떤 활동과 연결되는가?
- 수 체계와 표기 체계는 어떤 관계를 보이는가?
- 문자 발생을 단일한 '발명 순간'으로 설명하는 것이 적절한가?
- 행정 기록에서 언어적 문장 기록으로의 변화는 어떻게 추적할 수 있는가?

## 완료 조건
- Source Pack의 모든 항목이 원 출처와 안정 식별자로 되돌아갈 수 있다.
- 핵심 주장에는 실제 자료 또는 명시적인 현대 연구 근거가 연결된다.
- 학습용 설명과 연구용 증거 레이어가 분리된다.
- 초보자가 같은 질문으로 첫 Context Package를 생성할 수 있다.
- 검색 결과와 인용 범위를 재현할 수 있다.
- Context Package의 역사적 해석이 관련 분야 검토를 받는다.

## 다음 작업

1. `P002718`, `P000014`, `P000021`의 판본·transliteration·장르를 사람 검토한다.
2. Context Package 초안을 `source_checked`로 승격할 수 있는 기준을 적용한다.
3. Uruk IV 자료와 대표 PCSL sign을 포함하는 Source Pack v0.2를 만든다.
4. earliest writing과 Uruk III 기록 문화의 차이를 초보자 설명에 반영한다.
5. 학습 화면에서 증거·해석·불확실성을 분리해 표시한다.

## 다음 연구와의 연결
R002 완료 후 R001 `신아시리아 제국은 어떻게 거대한 영토를 통치했는가?`로 확장하여 왕실 비문, 편지, 조약, 행정자료처럼 서로 다른 장르의 교차 검색을 시험한다.
