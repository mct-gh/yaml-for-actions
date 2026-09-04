## 🎉 완주했습니다

여러분이 만든 것:

- 파이썬 자료구조로 이해한 YAML 문법 (매핑·시퀀스·스칼라·앵커)
- `name` / `on` / `jobs` / `steps` 워크플로 스키마
- `run` vs `uses`, 버전 고정, `env` vs `with`
- `${{ }}` 표현식과 컨텍스트, 셸 인젝션 회피
- `id` → `outputs` → `needs` → `if` 데이터 배관
- `matrix` 병렬화와 `permissions` 최소 권한

### 다음에 볼 것

- [Workflow syntax 레퍼런스](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [워크플로를 유발하는 이벤트](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- 재사용: composite action(step 묶음) vs reusable workflow(job 묶음)
- `actionlint`를 pre-commit에 걸어 YAML 오류를 커밋 전에 잡기
