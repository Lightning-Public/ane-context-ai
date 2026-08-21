# 데이터 소스 및 접근 전략

이 문서는 2026-08-21에 확인한 공식 안내를 기준으로 한 초기 전략이다. 웹에서 열람 가능하다는 사실은 자동 수집·재배포·모델 학습 허가를 뜻하지 않는다. 실제 수집 전에는 하위 프로젝트, 데이터 유형, 판본, 이미지별 조건을 다시 확인하고 `data/manifests/`에 스냅샷을 남긴다.

## 우선순위

| 소스 | 강점 | 초기 접근 | 저장소 정책 |
|---|---|---|---|
| ORACC | 주석된 설형문자 전사·번역·표제어·메타데이터 | 공식 JSON manifest/archive | 첫 수직 실험. 프로젝트별 권리 확인 후 허가된 텍스트 데이터만 로컬 캐시 |
| CDLI | 유물 중심 카탈로그, 사진, 전사, 소장 정보 | `cdli.earth` API/공식 클라이언트, 필요 시 공개 덤프 | 식별자 연결의 중심. 이미지는 권리 확인 전 저장·재배포 금지 |
| eBL | 바빌로니아 문학 텍스트, 파편·조인, 공개 API 생태계 | 공개 API와 명시적 공개 데이터 릴리스 | API 코드의 MIT와 코퍼스 콘텐츠 권리를 구분 |
| TLA | 이집트어 텍스트·어휘·번역·주석 | 웹의 허용된 개별 참조, 공식 공개 데이터 릴리스 | 기본적으로 링크·인용만. 대량 수집 금지 |

## ORACC

### 공식 진입점

- [Open Data 안내](https://oracc.museum.upenn.edu/doc/opendata/)
- [JSON 형식 안내](https://oracc.museum.upenn.edu/doc/opendata/json/)
- [JSON 다운로드 목록](https://oracc.museum.upenn.edu/json/)
- [공개 프로젝트 목록](https://oracc.museum.upenn.edu/projects.json)

### 접근 방식

1. `projects.json`에서 공개 프로젝트를 발견한다.
2. 프로젝트의 `manifest.json`으로 실제 제공 파일을 확인한다.
3. `catalogue.json`으로 문헌 ID, 시대, 출토지, 장르, 언어 등 메타데이터를 가져온다.
4. `corpus.json` 또는 문헌별 JSON에서 행·단어·표제어·번역 구조를 가져온다.
5. 원 ZIP/JSON의 URL, 획득 시각, SHA-256, 프로젝트명, 판본/업데이트 정보를 기록한다.

### 라이선스 판단

ORACC의 일반 콘텐츠는 별도 표시가 없으면 CC BY-SA 3.0으로 안내된다. 일부 공식 교육 자료는 ORACC JSON을 CC0로 설명하고, OSL처럼 개별 데이터셋이 CC0를 명시하기도 한다. 따라서 이 프로젝트는 **ORACC 전체를 일괄 CC0로 간주하지 않는다**.

- 페이지·프로젝트·다운로드에 명시된 조건을 우선한다.
- 명시가 없으면 ORACC 기본 CC BY-SA 3.0을 보수적으로 적용한다.
- CC0는 해당 배포물이 명시적으로 CC0라고 밝힌 경우에만 기록한다.
- 저자, 편집자, 프로젝트명, 원 URL, 접근일을 파생 레코드에 유지한다.

## CDLI

### 공식 진입점

- [CDLI](https://cdli.earth/)
- [공식 Framework API Client](https://github.com/cdli-gh/framework-api-client)
- [공개 카탈로그·ATF 덤프 저장소](https://github.com/cdli-gh/data)

공식 클라이언트는 카탈로그와 텍스트를 CSV, TSV, NDJSON, N-Triples, Turtle, BibTeX, ATF 등으로 내보내는 흐름을 문서화한다. 공개 덤프 저장소는 카탈로그와 ATF를 제공하지만 README에 마지막 업데이트가 2022년 8월이라고 표시되어 있으므로 최신성 확인 없이 기준 데이터로 삼지 않는다.

### 접근 방식

- 라이브 API를 작은 범위로 조회하고 응답 버전·시각·쿼리를 기록한다.
- 대량 분석이 필요할 때만 공식 export 도구 또는 명시된 덤프를 사용한다.
- P-number 등 안정 식별자를 ORACC/eBL의 외부 식별자와 연결하되, 동일성은 근거 있는 주장으로 저장한다.
- 사진과 3D 자산은 소장 기관·촬영자·개별 자산의 권리 조건을 별도로 확인한다.

### 라이선스 판단

API 클라이언트의 오픈소스 라이선스는 CDLI 데이터·사진의 라이선스가 아니다. 현재의 첫 커밋에서는 CDLI 데이터를 재배포하지 않는다. 데이터 유형별 명시적 이용 조건을 확인할 때까지 메타데이터 링크와 식별자만 저장하는 것을 기본값으로 한다.

## eBL (Electronic Babylonian Library)

### 공식 진입점

- [eBL](https://www.ebl.lmu.de/)
- [eBL GitHub 조직](https://github.com/ElectronicBabylonianLiterature)
- [eBL API 소스](https://github.com/ElectronicBabylonianLiterature/ebl-api)

### 접근 방식

- 공개 읽기 API의 문서화된 엔드포인트만 사용한다.
- 파편(fragment), 작품(composition), 전사, 조인(join)의 식별자를 구분한다.
- 대량 획득은 eBL이 공개한 데이터셋·도구와 해당 릴리스의 인용·라이선스 조건을 따른다.
- 응답 원본을 영구 재배포하기 전에 콘텐츠 라이선스를 별도로 확인한다.

### 라이선스 판단

`ebl-api` 소스 코드는 MIT 라이선스이지만, 이것이 API가 제공하는 모든 텍스트·사진·번역을 MIT로 허가한다는 뜻은 아니다. 코드, API 응답, 공개 연구 데이터셋, 이미지의 권리를 각각 기록한다.

## TLA (Thesaurus Linguae Aegyptiae)

### 공식 진입점

- [TLA](https://thesaurus-linguae-aegyptiae.de/)
- [라이선스 안내](https://tla.digital/info/licenses)
- [TLA GitHub 조직](https://github.com/thesaurus-linguae-aegyptiae)

### 접근 방식과 제한

공식 라이선스 안내는 학술 연구를 위한 개별 데이터셋의 복사·인용을 허용하지만, 전체 하위 코퍼스 또는 10개 웹페이지를 넘는 큰 묶음의 복사는 허용하지 않는다고 밝힌다. 향후 별도의 자유 라이선스로 원시 데이터가 공개될 수 있다고 안내한다.

따라서 초기 정책은 다음과 같다.

- 웹페이지 스크래핑이나 코퍼스 복제를 하지 않는다.
- 허용 범위의 개별 레코드는 정확한 인용과 접근일을 포함한다.
- 대량 사용은 공식 공개 데이터 릴리스의 개별 라이선스를 따르거나 서면 허가를 받는다.
- 웹 애플리케이션 소스의 Apache-2.0 등 소프트웨어 라이선스를 과학 데이터에 확장 적용하지 않는다.

## 소스 매니페스트 필수 필드

각 획득 단위는 최소한 다음을 기록한다.

```json
{
  "source_id": "oracc:PROJECT",
  "source_name": "Human-readable project name",
  "source_url": "https://...",
  "retrieved_at": "RFC-3339 timestamp",
  "source_version": "release, commit, or observed update",
  "content_scope": ["catalogue", "transliteration"],
  "license": {
    "expression": "SPDX or LicenseRef",
    "evidence_url": "https://...",
    "verified_at": "RFC-3339 timestamp",
    "notes": "dataset-specific limits"
  },
  "citation": "required attribution text",
  "acquisition": {
    "method": "api|archive|manual",
    "query_or_path": "...",
    "sha256": "..."
  },
  "redistribution": "allowed|restricted|unknown"
}
```

`redistribution`이 `unknown` 또는 `restricted`이면 원 데이터를 Git에 커밋하지 않는다. 변환 산출물도 원 저작물을 실질적으로 재구성할 수 있으면 같은 제한을 적용한다.

## 획득 전 체크리스트

- [ ] 공식 출처인가?
- [ ] 데이터와 소프트웨어 라이선스를 구분했는가?
- [ ] 하위 프로젝트·판본·이미지별 예외가 있는가?
- [ ] 대량 접근, 캐시, 재배포가 각각 허용되는가?
- [ ] 저자·편집자·기관·영구 식별자·접근일을 기록했는가?
- [ ] robots.txt, 이용약관, 속도 제한, 인증 요구를 준수하는가?
- [ ] 삭제 또는 조건 변경 시 해당 레코드를 추적할 수 있는가?
