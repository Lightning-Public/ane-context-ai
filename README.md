# ANE Context AI

고대근동(Ancient Near East)의 문헌·유물·연대·지리·학계 논쟁을 질문별 **Context Package**로 엮는 오픈 연구·학습 프로젝트입니다.

> AI를 정답 기계가 아니라, 서로 다른 증거와 해석을 출처·불확실성과 함께 연결하는 컨텍스트 엔진으로 사용합니다.

## 목표

사용자의 질문을 받으면 다음 요소를 한 묶음으로 구성하는 시스템을 지향합니다.

- 질문의 시간·공간·언어·장르 범위
- 일차 사료의 원문, 전사, 번역, 유물 식별자와 판본
- 인물·장소·정체·시대·문헌 사이의 관계
- 서로 지지하거나 충돌하는 증거와 해석
- 학계의 합의, 주요 논쟁, 미해결점
- 검색 시점과 경로를 재현할 수 있는 출처 기록

이 프로젝트는 단일한 “정답”을 생성하거나 AI 번역을 학술 판본처럼 제시하지 않습니다. 성경과 고대근동 자료의 유사성도 직접 영향으로 성급히 단정하지 않고, 공통 문화권·장르 관습·독립 발전 등 대안 가설을 함께 검토합니다.

## Context Package 흐름

```text
질문
  → 범위·용어·연대 체계 명시
  → 허가된 데이터 소스 검색
  → 문헌 단위와 유물 단위 식별자 연결
  → 관련 구절·메타데이터·학술 해석 검색(RAG)
  → 인물·장소·시대·관계 탐색(Knowledge Graph)
  → 증거 / 해석 / 논쟁 / 불확실성 분리
  → AI-assisted audit
  → 사람의 판본·행·권리 검토
  → 인용 가능한 Context Package
  → 초보자용 Learning View Model과 학습 화면
```

## 현재 상태

- `ANE 101` 초보자 온보딩 Module 0–3 초안
- `R002 — 문자는 왜 탄생했는가?` 연구 파일럿
- Uruk III 후보 24건의 CDLI live resolution 완료: 24/24 resolved
- 첫 source-linked Context Package 상태: `needs_revision`
- CDLI 검증기, Context Package 검증기, GitHub Actions 테스트
- 사람 전문가 검토 없이 `source_checked` 또는 artifact `verified`로 승격할 수 없는 review gate
- 첫 초보자용 정적 학습 화면과 provenance-preserving Learning View Model

실제 외부 이미지와 대량 코퍼스 원본은 저장소에 포함하지 않습니다. 식별자·허용된 짧은 전사 인용·출처 및 권리 manifest를 중심으로 관리합니다.

## 첫 학습 화면 실행

저장소 루트에서 간단한 정적 서버를 실행합니다.

```bash
python -m http.server 8000
```

브라우저에서 다음 주소를 엽니다.

```text
http://localhost:8000/web/r002/
```

화면은 `examples/r002-origin-of-writing.context-package.json`을 직접 읽고 다음 층위를 분리해 표시합니다.

- 지도와 연대표
- 유물 신원과 전사
- 자료가 직접 보여주는 내용
- 비교를 통해 도출한 제한적 결론
- 현대 학자의 해석
- 논쟁과 불확실성
- provenance와 사람 검토 상태

현재 패키지는 `needs_revision`이므로 화면도 이를 상단에 명시하고 각 자료를 `verified 아님`으로 표시합니다. CDLI 사진이나 line art는 복제하지 않습니다.

## 빠른 시작

Python 3.11 이상만 필요합니다.

```bash
PYTHONPATH=src python -m ane_context_ai validate examples/context-package.example.json
PYTHONPATH=src python -m ane_context_ai validate-review \
  examples/r002-ai-source-audit.review-record.json
PYTHONPATH=src python -m unittest discover -s tests
```

패키지를 개발 모드로 설치하면 `ane-context` 명령을 사용할 수 있습니다.

```bash
python -m pip install -e .
ane-context validate examples/context-package.example.json
ane-context validate-review examples/r002-ai-source-audit.review-record.json
```

Context Package에서 학습용 View Model 생성:

```bash
ane-context build-learning-view \
  examples/r002-origin-of-writing.context-package.json \
  --output /tmp/r002-learning-view.json
```

사람 검토를 받은 Context Package 승격 검증:

```bash
ane-context validate-promotion path/to/package.json \
  --review-record path/to/human-review.json
```

artifact `verified` 승격 검증:

```bash
ane-context validate-source-pack data/manifests/source-pack.json \
  --review-record path/to/artifact-review.json
```

## 저장소 구조

```text
.
├── README.md
├── PROJECT.md                 범위, 로드맵, 성공 기준
├── DATA-SOURCES.md            ORACC/CDLI/eBL/TLA 접근·권리 전략
├── RESEARCH-METHOD.md         사료비판 및 연구 절차
├── docs/
│   ├── onboarding/            ANE 101 학습 모듈
│   ├── research/              연구 주제와 실행 기록
│   ├── product/               학습 화면·제품 계약
│   ├── architecture.md        RAG + Knowledge Graph 설계
│   ├── context-package.md     결과물 계약
│   ├── review-workflow.md     사람 검토·승격 게이트
│   └── data-governance.md     출처·라이선스·삭제 정책
├── data/
│   ├── manifests/             소스별 획득·권리·버전 기록
│   ├── raw/                   변경하지 않은 원본(커밋 금지)
│   ├── interim/               중간 산출물(커밋 금지)
│   └── processed/             파생 데이터(기본 커밋 금지)
├── schemas/
│   ├── context-package.schema.json
│   └── review-record.schema.json
├── templates/                 검토 기록 등 기여 템플릿
├── examples/                  합성 및 연구 예시
├── src/ane_context_ai/        검증·획득·View Model 도구
├── web/r002/                  첫 초보자용 정적 학습 화면
└── tests/
```

## 핵심 원칙

1. **출처 우선** — 모든 주장과 인용은 안정적인 식별자와 원 출처로 되돌아갈 수 있어야 합니다.
2. **층위 분리** — 유물, 전사, 번역, 현대 해석, AI 추론을 같은 사실처럼 섞지 않습니다.
3. **불확실성 보존** — 추정 연대, 출토지, 복원 문자, 논쟁적 동일시는 범위와 근거를 남깁니다.
4. **라이선스 우선** — 접근 가능성과 재사용 가능성을 구분하고, 소스·자료 유형별 조건을 기록합니다.
5. **재현 가능성** — 획득 시점, 버전, 쿼리, 변환 코드, 모델과 프롬프트를 기록합니다.
6. **인간 검토 게이트** — API resolution과 AI audit은 문제를 찾을 수 있지만, 사람을 대신하여 `source_checked`, `expert_reviewed`, `verified`를 부여할 수 없습니다.
7. **검토 이력 보존** — 누가 어떤 판본·도판·행을 확인했는지 별도 review record로 Git에 남깁니다.
8. **학습 화면도 provenance 유지** — 초보자에게 쉽게 보여 주더라도 source ID, locator, claim status, review state를 제거하지 않습니다.

## 문서 안내

- [프로젝트 계획](PROJECT.md)
- [데이터 소스 전략](DATA-SOURCES.md)
- [연구 방법과 사료비판](RESEARCH-METHOD.md)
- [학습 경로](docs/learning-path.md)
- [첫 학습 화면 계약](docs/product/first-learning-screen.md)
- [아키텍처](docs/architecture.md)
- [Context Package 규격](docs/context-package.md)
- [사람 검토와 승격](docs/review-workflow.md)
- [데이터 거버넌스](docs/data-governance.md)

## 라이선스

프로젝트가 작성한 코드와 문서는 [Apache License 2.0](LICENSE)으로 배포합니다. 외부 코퍼스, 번역, 이미지, 메타데이터에는 각각의 원 권리와 이용 조건이 적용됩니다. Apache-2.0은 외부 데이터의 재배포 권한을 부여하지 않습니다.
