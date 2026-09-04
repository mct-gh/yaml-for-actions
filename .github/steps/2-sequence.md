## Step 2: `-`는 파이썬 list다

`steps:`는 리스트입니다. `-` 하나가 step 하나이고, `steps:` 아래 키는 dict가 아니라 **list of dict**가 됩니다.

```yaml
steps:                        # "steps": [
  - name: 첫 번째              #   {"name": "첫 번째", "run": "echo hi"},
    run: echo hi              #   {"name": "두 번째", "run": "echo bye"}
  - name: 두 번째              # ]
    run: echo bye
```

- `step:`이라는 키는 존재하지 않습니다. 항상 복수형 `steps:` + `-`입니다.
- `-` 다음 줄들은 들여쓰기만 맞으면 같은 step에 속합니다 (`run`, `name`, `env` 등).
- step은 위에서 아래로 **순차 실행**되고, 같은 러너·같은 파일시스템을 공유합니다.

### ⌨️ 할 일

`practice.yml`의 job에 `steps:`를 추가하고, `name`이 붙은 step을 **2개 이상** 만드세요.

<details><summary>정답 보기</summary>

```yaml
    steps:
      - name: Say hello
        run: echo "Hello, Actions!"
      - name: Say goodbye
        run: echo "Bye!"
```
</details>
