## Step 5: `env`와 `with` — 값 주입의 두 통로

이름이 비슷하지만 목적지가 다릅니다.

| 키 | 어디로 가나 | 파이썬 비유 |
|---|---|---|
| `env:` | 프로세스 **환경변수** → `os.getenv()` | 전역 설정 |
| `with:` | **action의 입력 파라미터** | 함수 인자 |

```yaml
jobs:
  tell:
    env:
      FORTUNE_FOR: Mona          # 이 job의 모든 step에 적용
    steps:
      - uses: actions/setup-python@v5
        with:                    # 이 action에만 전달
          python-version: "3.12"
      - run: python scripts/fortune.py
        env:
          FORTUNE_FOR: Hubot     # 이 step에서만 덮어씀 (좁은 스코프 우선)
```

스코프는 `workflow → job → step` 순으로 좁아지고, 좁은 쪽이 이깁니다. 파이썬의 전역/지역 변수와 같습니다.

`fortune.py`는 `os.getenv("FORTUNE_FOR", "Octocat")`으로 이 값을 읽습니다.

### ⌨️ 할 일

`FORTUNE_FOR` 환경변수를 정의해서 운세의 주인 이름을 바꾸세요.

<details><summary>정답 보기</summary>

```yaml
      - name: Run fortune
        run: python scripts/fortune.py
        env:
          FORTUNE_FOR: Mona
```
</details>
