## Step 3: `run` vs `uses`

step은 둘 중 하나입니다. 섞어 쓸 수 없습니다.

| 키 | 뜻 | 파이썬 비유 |
|---|---|---|
| `run:` | 러너의 셸에서 명령 실행 | 코드를 직접 작성 |
| `uses:` | 남이 만든 **action** 호출 | `import` 후 함수 호출 |

```yaml
- uses: actions/checkout@v5        # 레포를 러너로 내려받음
- uses: actions/setup-python@v5    # 파이썬 설치
  with:
    python-version: "3.12"
- run: python scripts/fortune.py
```

- `@v5`는 **버전 고정(pinning)**. 생략하면 실행 자체가 거부됩니다. 보안이 중요하면 커밋 SHA로 고정합니다.
- `actions/checkout`을 넣지 않으면 러너에는 여러분의 코드가 없습니다. 대부분의 "파일을 못 찾음" 오류의 원인입니다.

### ⌨️ 할 일

`checkout@v5`, `setup-python@v5`, 그리고 `run` step을 각각 넣으세요.

<details><summary>정답 보기</summary>

```yaml
    steps:
      - name: Checkout
        uses: actions/checkout@v5
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Run fortune
        run: python scripts/fortune.py
```
</details>
