## Step 4: 여러 줄과 따옴표 — 스칼라의 함정

값 하나(스칼라)를 쓰는 방법이 여러 가지이고, 선택에 따라 파이썬 타입이 바뀝니다.

```yaml
run: |            # 개행 유지 → "pip install -r req.txt\npython app.py\n"
  pip install -r requirements.txt
  python scripts/fortune.py

desc: >           # 개행을 공백으로 접음 → "긴 문장을 한 줄로 만든다\n"
  긴 문장을
  한 줄로 만든다
```

**가장 자주 터지는 사고 두 가지**

| 쓴 것 | 파이썬 타입 | 결과 |
|---|---|---|
| `python-version: 3.10` | `float` 3.1 | 파이썬 **3.1**을 찾다 실패 |
| `python-version: "3.10"` | `str` | 정상 |

`${{ }}`로 시작하는 값도 반드시 따옴표로 감싸세요. `{`는 YAML에서 flow mapping 시작 문자라 파싱이 깨집니다.

### ⌨️ 할 일

1. `|` 블록으로 여러 줄 `run:`을 만들고 그 안에서 `scripts/fortune.py`를 실행하세요.
2. `python-version` 값을 **문자열**로 바꾸세요.

<details><summary>정답 보기</summary>

```yaml
      - name: Run fortune
        run: |
          python --version
          python scripts/fortune.py
```
</details>
