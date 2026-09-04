# YAML for GitHub Actions — 파이썬 개발자를 위한 실습

_파이썬의 dict / list 로 YAML을 이해하고, 워크플로 문법을 8단계로 완성합니다._

## Welcome

- **대상**: 파이썬은 알지만 GitHub Actions YAML은 처음인 학습자
- **배우는 것**: YAML 문법의 뿌리 → Actions 워크플로 스키마 → 표현식·매트릭스까지
- **만드는 것**: PR에 오늘의 운세를 남기는 **Octo-Fortune Bot** 워크플로
- **선행**: Git 기본, Python 기본 문법
- **소요 시간**: 약 45분

이 실습에서 여러분은:

1. YAML 매핑이 파이썬 `dict`이고 `-` 리스트가 `list`임을 코드로 확인합니다.
2. `name` / `on` / `jobs` 3대 최상위 키로 워크플로 뼈대를 세웁니다.
3. `run`과 `uses`의 차이, 액션 버전 고정(pinning)을 익힙니다.
4. 블록 스칼라 `|`, `>`와 따옴표 규칙으로 여러 줄 파이썬을 실행합니다.
5. `env` / `with` 로 값을 주입하고 스코프를 이해합니다.
6. `${{ }}` 표현식과 `github` / `secrets` 컨텍스트를 씁니다.
7. `id` → `outputs` → `needs` → `if` 로 job 사이에 값을 넘깁니다.
8. `strategy.matrix`와 `permissions`로 병렬 실행과 최소 권한을 적용합니다.

> [!NOTE]
> 각 단계는 여러분이 작성한 `.github/workflows/practice.yml`을
> **파이썬 검증기(`.github/script/verify.py`)** 가 PyYAML로 파싱해서 채점합니다.
> 즉, YAML을 배우면서 동시에 "YAML은 결국 파이썬 자료구조"라는 걸 눈으로 봅니다.

## 시작하는 법

1. 이 저장소를 **Use this template → Create a new repository** 로 복사합니다 (public 권장).
2. 약 20초 후 새로고침하면 첫 단계가 이슈로 열립니다.
3. 이슈의 안내대로 `.github/workflows/practice.yml`을 고치고 `main`에 push 하면 자동 채점됩니다.

전체 설계와 흐름은 [OUTLINE.md](OUTLINE.md)를 보세요.
