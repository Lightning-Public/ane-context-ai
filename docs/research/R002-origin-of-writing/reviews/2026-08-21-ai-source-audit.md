# R002 source review — 2026-08-21

## 대상

첫 Context Package가 사용한 세 CDLI artifact를 출처 수준에서 다시 점검했다.

- `P002718` — ATU 3, pl. 078, W 17729,cn+
- `P000014` — ATU 3, pl. 036, W 12139
- `P000021` — ATU 3, pl. 080, W 13948

검토자는 `OpenAI GPT-5.6 Pro (source-audit assistant)`이며, 이 기록은 Assyriologist의 전문가 검토를 대체하지 않는다.

## 검토 자료

- CDLI artifact pages와 현재 catalogue metadata
- CDLI transliteration history 및 revisions/credits
- CDLI가 연결한 primary publication references
- Englund, Nissen, with Damerow 1993, *Die lexikalischen Listen der archaischen Texte aus Uruk* (ATU 3)
- Peter Damerow 2006, “The Origins of Writing as a Problem of Historical Epistemology,” CDLJ 2006:1

## 결과

| ID | CDLI 현재 분류 | 소장·번호 | 일차 출판 | 전사 최신 책임 | 판정 |
|---|---|---|---|---|---|
| `P002718` | Uruk III; Uruk; Administrative | National Museum of Iraq; `IM 046049 ?` | ATU 3, pl. 78 | Robert K. Englund, approved 2018-02-12 | metadata 확인, 장르 재검토 필요 |
| `P000014` | Uruk III; Uruk; Lexical, Archaic Pigs witness | Vorderasiatisches Museum; `VAT 16773` | ATU 3, pl. 36 | Robert K. Englund, approved 2016-04-12 | metadata 확인, 도판 collation 필요 |
| `P000021` | Uruk III; Uruk; Lexical > Vocabularies | Vorderasiatisches Museum; `VAT 16972` | ATU 3, pl. 80 | Robert K. Englund, approved 2015-11-18 | metadata 확인, 도판 collation 필요 |

이전 전사 이력에는 Jacob L. Dahl과 CDLI의 판본이 포함된다.

## 수정한 오류

기존 Context Package의 짧은 전사 인용에서 손상·불확실성 표시가 일부 누락되어 있었다.

- `P002718`: `DUR2#`, `BU3#`, `|SZE~a&SZE~a|#?`의 표지를 복원
- `P000014`: `U4 SZUBUR#`의 `#`를 복원
- `P000021`: `U4#`를 복원하고 locator를 실제 인용한 1–5행과 일치시킴
- `[...]`, `X`, `?`, `#`를 현대어 문장처럼 매끄럽게 제거하지 않도록 review uncertainty에 명시

## 핵심 발견: P002718 장르 충돌

CDLI의 현재 catalogue는 `P002718`을 `Administrative`로 분류한다. 그러나 같은 entry에는 Foreign ID `LGE 5`가 있고 ATU 3 관련 주석에는 `Geography 5`가 표시된다. 이 자료가 순수한 행정문서인지, archaic geographical list와 연결되는 witness인지, 또는 catalogue 층위가 다른 것인지 전문가 검토가 필요하다.

따라서 `P002718`을 명확한 “행정문서 대 lexical list” 비교축으로 사용하는 현재 설계는 아직 확정할 수 없다.

## 학술적 해석 보강

Damerow 2006의 §§5–10을 추가했다.

- 대다수 proto-cuneiform 자료를 경제·행정적 bookkeeping으로 설명
- lexical lists를 school texts로 구분
- 동시에 lexical lists의 의미 범주도 행정적 기록의 제한된 semantic categories와 연결
- tokens, seals, standardized containers 등 선행 행정 장치와 proto-cuneiform의 연속성을 강조
- proto-writing이 처음부터 구어 언어 전체를 표기하려 했다는 선형적 가정을 경계

따라서 “행정 때문에 문자가 발명되었다”와 “lexical list가 있으니 행정 기원설은 틀렸다”라는 양극단을 모두 피해야 한다.

## 판정

**`needs_revision`**

다음 이유로 `source_checked`로 승격하지 않는다.

1. `P002718`의 장르·기능 분류가 해결되지 않았다.
2. ATU 3 실제 도판을 독립적으로 collate하지 못했다.
3. 선택한 전사 행의 sign readings를 Assyriologist가 확인하지 않았다.
4. 세 자료는 Uruk III의 편의 표본으로 최초 문자 단계 전체를 대표하지 않는다.
5. 현재 검토자는 AI source-audit assistant이며 사람 전문가 검토가 아니다.

## 다음 조치

1. `P002718`의 LGE 5 / Geography 5 관계를 DCCLT·ATU 3 본문·전문가 검토로 해결
2. ATU 3 pl. 36, 78, 80 도판과 CDLI 현재 전사를 line-by-line collate
3. 명확한 administrative comparator가 필요하면 Source Pack v0.1의 다른 후보로 교체
4. Uruk IV 자료와 숫자·계량 표기를 Source Pack v0.2에 추가
5. 검토 결과에 따라 Context Package를 `source_checked` 또는 계속 `needs_revision`으로 결정

## 출처

- https://cdli.earth/P002718
- https://cdli.earth/P000014
- https://cdli.earth/P000021
- https://cdli.earth/publications/1785922
- https://cdli.earth/articles/cdlj/2006-1
