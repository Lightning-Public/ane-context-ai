# Data workspace

이 폴더는 외부 코퍼스의 복제 저장소가 아니다. 실제 데이터는 권리 검토와 소스 매니페스트 승인 후 로컬에서 획득하며 기본적으로 Git에 커밋하지 않는다.

```text
manifests/   출처, 라이선스, 버전, 쿼리, 체크섬
raw/         변경하지 않은 획득물
interim/     파싱·정규화 중간물
processed/   검색·그래프 입력용 파생물
```

새 데이터를 받기 전에 [DATA-SOURCES.md](../DATA-SOURCES.md)와 [데이터 거버넌스](../docs/data-governance.md)를 확인한다. 공개 가능한 작은 샘플이 필요하면 원문을 임의로 복사하지 말고 합성 데이터 또는 명시적으로 재배포 가능한 레코드를 사용한다.
