# Web prototypes

이 디렉터리는 Context Package 계약을 실제 학습 경험으로 검증하는 무빌드 정적 프로토타입을 둔다.

## R002 첫 학습 화면

### 로컬 검수

저장소 루트에서 실행한다.

```bash
python -m http.server 8000
```

브라우저에서 다음을 연다.

```text
http://localhost:8000/web/r002/
```

화면은 `examples/r002-origin-of-writing.context-package.json`을 읽어 브라우저에서 학습용 View Model로 변환한다. 외부 이미지·폰트·지도 서비스를 사용하지 않으며 CDLI 사진이나 line art를 복제하지 않는다.

백엔드·배치용 View Model은 다음 명령으로 만들 수 있다.

```bash
PYTHONPATH=src python -m ane_context_ai build-learning-view \
  examples/r002-origin-of-writing.context-package.json \
  --output /tmp/r002-learning-view.json
```

### 공유 미리보기

로컬 서버는 개발·시각 QA용이다. 다른 구성원과 PR 상태를 공유하려면 Vercel Preview를 사용한다.

저장소 루트의 `vercel.json`은 다음 공개 경로를 준비한다.

```text
/
/learn/origin-of-writing
```

두 경로 모두 첫 R002 학습 화면으로 연결된다. Vercel 프로젝트는 저장소 루트를 기준으로 정적 배포해야 하며, 별도 애플리케이션 서버나 환경변수는 현재 필요하지 않다.

자세한 설정은 [`docs/deployment/vercel.md`](../docs/deployment/vercel.md)를 따른다.

현재 패키지는 `needs_revision`이다. 로컬과 Vercel 화면 모두 해당 상태와 차단 문제를 그대로 표시하며 `resolved`를 `verified`로 표현하지 않는다.
