## Step 7: `id` → `outputs` → `needs` → `if`

job은 서로 다른 러너에서 **병렬로, 격리되어** 실행됩니다. 값을 넘기려면 명시적 배관이 필요합니다.

```yaml
jobs:
  draw:
    runs-on: ubuntu-latest
    outputs:
      fortune: ${{ steps.pick.outputs.text }}     # 3) job 밖으로 내보냄
    steps:
      - uses: actions/checkout@v5
      - id: pick                                   # 1) step에 이름표
        run: echo "text=$(python scripts/fortune.py)" >> "$GITHUB_OUTPUT"   # 2) 파일에 기록

  announce:
    needs: draw                                    # 4) 순서 + 값 접근권
    if: ${{ needs.draw.outputs.fortune != '' }}    # 5) 조건부 실행
    runs-on: ubuntu-latest
    steps:
      - run: echo "$MSG"
        env:
          MSG: ${{ needs.draw.outputs.fortune }}
```

- `id:`는 **참조가 필요할 때만** 답니다. `name:`은 사람이 읽는 라벨, `id:`는 코드가 쓰는 키입니다.
- step 출력은 `$GITHUB_OUTPUT` 파일에 `key=value`로 append 하는 방식입니다.
- `if:` 값은 이미 표현식 문맥이라 `${{ }}`를 생략해도 동작합니다.

### ⌨️ 할 일

job을 2개로 나누고, 첫 job의 운세를 두 번째 job에서 출력하세요. `if:` 조건도 하나 넣으세요.

<details><summary>정답 보기</summary>

위 예시를 그대로 쓰면 통과합니다.
</details>
