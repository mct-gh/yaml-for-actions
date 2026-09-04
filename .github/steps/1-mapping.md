## Step 1: YAML은 파이썬 dict다

YAML 파일 하나는 파이썬 자료구조 하나입니다. `key: value`는 dict의 항목이고, 들여쓰기는 중첩입니다.

```yaml
name: Octo-Fortune          # {"name": "Octo-Fortune",
on: workflow_dispatch       #  "on": "workflow_dispatch",
jobs:                       #  "jobs": {"tell": {"runs-on": "ubuntu-latest"}}}
  tell:
    runs-on: ubuntu-latest
```

기억할 3가지:
- **들여쓰기는 스페이스 2칸.** 탭은 문법 오류입니다 (파이썬보다 엄격).
- `#`은 주석. 값 뒤에 쓸 땐 앞에 공백 한 칸이 필요합니다.
- 워크플로 최상위 필수 키는 `name` / `on` / `jobs` 셋입니다. `on`은 "언제", `jobs`는 "무엇을".

> [!TIP]
> **함정 하나**: 파이썬 PyYAML로 이 파일을 읽으면 `on` 키가 문자열이 아니라 불리언 `True`가 됩니다.
> YAML 1.1이 `on/off/yes/no`를 불리언으로 취급하기 때문입니다. 이 실습의 채점기가 두 키를 모두 뒤지는 이유입니다.

### ⌨️ 할 일

1. `.github/workflows/practice.yml` 파일을 새로 만듭니다.
2. 위 예시처럼 `name`, `on`, `jobs`(job 1개 + `runs-on`)를 작성합니다.
3. `main` 브랜치에 커밋하고 push 합니다.

<details><summary>정답 보기</summary>

```yaml
name: Octo-Fortune
on: workflow_dispatch
jobs:
  tell:
    name: Tell a fortune
    runs-on: ubuntu-latest
```
</details>
