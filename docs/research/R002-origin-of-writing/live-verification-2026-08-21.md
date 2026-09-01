# R002 CDLI live verification — 2026-08-21

## 목적

`r002-source-pack-v0.1`의 24개 CDLI P-number가 현재 CDLI에서 실제로 해석되는지 확인하고, 정규화된 메타데이터를 첫 Context Package 초안으로 연결하기 위한 실행 기록이다.

## 실행

- 실행 시각: `2026-08-21T06:25:50Z`
- GitHub Actions workflow: `cdli-live-verify`
- workflow run: `32454347650`
- source pack: `data/manifests/r002-source-pack-v0.1.json`
- verifier: `src/ane_context_ai/cdli.py`, `src/ane_context_ai/cdli_manifest.py`
- API route: `GET https://cdli.earth/artifacts/{numeric-id}.json`

CDLI의 단일 artifact JSON route는 객체가 아니라 길이 1의 배열을 반환했다. verifier는 빈 배열 또는 복수 레코드를 임의 선택하지 않고 오류로 처리하며, 정확히 하나의 객체만 안전하게 해제한다.

## 결과 요약

| 항목 | 결과 |
|---|---:|
| 시도 | 24 |
| 현재 CDLI에서 해석됨 | 24 |
| 오류 | 0 |
| 후보 period와 명시적으로 일치 | 23 |
| CDLI period 누락 | 1 |
| provenience 누락 | 3 |
| provenience가 uncertain으로 기록됨 | 6 |
| Uruk (mod. Warka) provenience | 12 |
| Umma (mod. Tell Jokha) provenience | 3 |
| inscription 데이터 존재 표시 | 24 |

장르 분포는 다음과 같다.

- Administrative: 13
- Vocabularies: 9
- Lexical: 2

이 분포는 편의적으로 선택된 working set의 분포이며 Uruk III 전체 코퍼스의 통계로 사용할 수 없다.

## 검토가 필요한 예외

- `P499393`: CDLI 응답에서 period가 누락되어 후보의 `Uruk III`를 검증할 수 없음
- `P471695`, `P482082`, `P482083`: provenience 누락
- `P448701`, `P448702`, `P448703`, `P499393`, `P504412`, `P504413`: provenience가 `uncertain`으로 기록됨

누락 또는 충돌 값을 추정으로 채우지 않는다. 후보 선택 자료와 CDLI 현재 메타데이터가 다르면 두 주장을 별도 provenance와 함께 유지한다.

## 첫 Context Package용 자료 선정

첫 초안은 출토지와 기간이 명확하고 서로 다른 기록 기능을 비교할 수 있는 세 자료를 사용한다.

| CDLI ID | 기간 | 출토지 | 장르 | 선택 이유 |
|---|---|---|---|---|
| `P002718` | Uruk III | Uruk (mod. Warka) | Administrative | 행정 기록 사례 |
| `P000014` | Uruk III | Uruk (mod. Warka) | Lexical | lexical 분류 사례 |
| `P000021` | Uruk III | Uruk (mod. Warka) | Vocabularies | vocabulary 목록 사례 |

초안 위치: `examples/r002-origin-of-writing.context-package.json`

이 세 자료는 “문자가 행정 때문에 발명되었다”는 결론을 확정하기 위한 것이 아니다. 같은 시기·지역에서 행정, lexical, vocabulary 기록이 함께 존재한다는 사실을 이용해 다음을 구분하는 데 목적이 있다.

1. 자료가 직접 말해 주는 장르와 기록 행위
2. 기록 기능에 대한 제한적 비교
3. 문자 발생 원인에 대한 현대적 해석
4. 이 표본으로는 답할 수 없는 부분

## 권리 및 재사용 상태

CDLI Terms of Use와 REST API 문서를 확인한 결과:

- 사진은 소장 기관 등의 권리를 따르므로 저장소에 복제하지 않는다.
- line art는 해당 출판물 또는 저자 권리를 따르므로 복제하지 않는다.
- transliteration과 translation은 학술적 관행과 출처 표기를 전제로 재사용할 수 있다고 안내된다.
- catalogue metadata 전체에 적용되는 단일 명시 라이선스는 확인하지 못했으므로 최소 식별자·인용 메타데이터만 저장한다.

관련 manifest: `data/manifests/cdli-terms-2026-06-13.json`

공식 문서:

- https://cdli.earth/terms-of-use
- https://cdli.earth/docs/api

## 현재 상태

24건은 모두 `resolved`되었지만 자동으로 `verified`로 승격하지 않는다. 다음 검토가 끝나야 승격할 수 있다.

- period/provenience/genre의 사람 검토
- 자료별 판본과 transliteration 책임 주체 확인
- 텍스트·이미지·메타데이터 권리의 분리 확인
- 첫 Context Package 주장에 대한 고대근동 연구자 검토

## 다음 작업

1. 새 Context Package JSON을 schema 및 semantic validator로 검사한다.
2. `P002718`, `P000014`, `P000021`의 artifact page와 판본을 사람 검토한다.
3. 초보자용 설명 레이어를 Context Package와 분리해 추가한다.
4. Uruk IV 자료를 포함하는 Source Pack v0.2를 설계한다.
5. earliest writing과 Uruk III 기록 문화의 차이를 명시적으로 비교한다.
