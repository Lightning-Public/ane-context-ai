# Vercel preview deployment

현재 `web/r002/` 프로토타입은 HTML, CSS, 브라우저 JavaScript만 사용하는 정적 사이트다. 별도 애플리케이션 서버나 데이터베이스는 필요하지 않다.

## 역할 분리

- 로컬 HTTP 서버: 개발자와 연구자의 빠른 시각·접근성 검수
- Vercel Preview: PR과 브랜치를 다른 사람에게 공유하고 피드백 수집
- Vercel Production: `main`에 병합된 안정 버전 공개

## 로컬 실행

저장소 루트에서 실행한다.

```bash
python -m http.server 8000
```

```text
http://localhost:8000/web/r002/
```

## Vercel 프로젝트 설정

GitHub 저장소 `Lightning-Public/ane-context-ai`를 Vercel의 새 프로젝트로 가져온다.

권장 설정:

- Production Branch: `main`
- Framework Preset: `Other`
- Root Directory: 저장소 루트 `.`
- Build Command: 비워 둠
- Output Directory: `.`
- Install Command: 비워 둠
- Environment Variables: 현재 없음

저장소 루트의 `vercel.json`이 다음 경로를 제공한다.

- `/` → `/web/r002/index.html`
- `/learn/origin-of-writing` → `/web/r002/index.html`

프로토타입은 저장소 루트의 Context Package fixture를 읽으므로 Vercel 프로젝트 Root Directory를 `web/r002`로 좁히지 않는다.

## 배포 상태 해석

Vercel 배포 성공은 웹 파일이 정상 제공된다는 뜻일 뿐, 연구 자료가 학술적으로 `verified` 또는 `source_checked`라는 뜻이 아니다.

화면은 Context Package의 review 상태를 그대로 표시해야 한다. 현재 R002 패키지는 `needs_revision`이며, Vercel Preview에서도 이 경고를 숨기지 않는다.

## 보안과 권리

- CDLI 이미지와 line art를 배포 산출물에 복제하지 않는다.
- 공개 저장소에 없는 비밀값을 환경변수로 추가하지 않는다.
- Context Package의 source URL, locator, 권리 manifest ID를 유지한다.
- 향후 외부 API를 브라우저에서 직접 호출할 경우 CORS, rate limit, 키 노출을 별도로 설계한다.

## 공개 전 확인

- 데스크톱과 모바일 레이아웃
- 키보드 탐색과 focus 표시
- 브라우저 콘솔 오류
- Context Package JSON 로딩
- source link와 locator
- `needs_revision`, `verified 아님`, 사람 검토 부재 표시
- 제한된 외부 이미지가 포함되지 않았는지 확인

공식 참고 문서:

- https://vercel.com/docs/git
- https://vercel.com/docs/builds
- https://vercel.com/docs/project-configuration/vercel-json
