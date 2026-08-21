# Web prototypes

이 디렉터리는 Context Package 계약을 실제 학습 경험으로 검증하는 무빌드 정적 프로토타입을 둔다.

## R002 첫 학습 화면

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

현재 패키지는 `needs_revision`이다. 이 프로토타입은 해당 상태와 차단 문제를 그대로 표시하며 `resolved`를 `verified`로 표현하지 않는다.
