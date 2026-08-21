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

## v0.1 Source Pack
처음부터 대량 코퍼스를 수집하지 않는다. 20~50건의 소규모 고품질 자료 묶음을 만든다.

현재 작업본:
- [Source Pack v0.1 — Uruk III working set](source-pack-v0.1.md)
- [Machine-readable manifest](../../../data/manifests/r002-source-pack-v0.1.json)

첫 작업본은 24개 CDLI P-number를 `candidate` 상태로 고정했다. 이 목록은 파이프라인 검증용 재현 가능한 working set이며 대표 표본이 아니다. 최신 CDLI 메타데이터와 권리 상태를 확인한 항목만 `verified`로 승격한다.

목표 구성:
- 초기 점토판 10~20건 이상
- 대표 숫자·기호 또는 표기 사례 5~10건
- 고고학·연대 Context 5건 내외
- 현대 학술 해설·개론 5~10건
- Uruk III뿐 아니라 Uruk IV 자료를 포함한 층화 표본

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

## 다음 연구와의 연결
R002 완료 후 R001 `신아시리아 제국은 어떻게 거대한 영토를 통치했는가?`로 확장하여 왕실 비문, 편지, 조약, 행정자료처럼 서로 다른 장르의 교차 검색을 시험한다.
