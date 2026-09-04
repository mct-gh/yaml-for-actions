## Step 6: `${{ }}` 표현식과 컨텍스트

`${{ }}`는 **실행 직전에 값으로 치환되는 자리**입니다. 파이썬 f-string과 같은 역할입니다.

자주 쓰는 컨텍스트:

| 컨텍스트 | 예 | 내용 |
|---|---|---|
| `github` | `${{ github.actor }}` | 실행을 유발한 사용자, 레포, 이벤트 페이로드 |
| `secrets` | `${{ secrets.GITHUB_TOKEN }}` | 암호화 저장된 값 (로그에 `***`로 마스킹) |
| `env` | `${{ env.FORTUNE_FOR }}` | 위에서 정의한 환경변수 |
| `runner` | `${{ runner.os }}` | 러너 OS |

```yaml
      - run: python scripts/fortune.py
        env:
          FORTUNE_FOR: ${{ github.actor }}
```

> [!WARNING]
> `run:` 안에 `${{ github.event.* }}` 같은 **사용자 입력**을 직접 넣으면 셸 인젝션 위험이 있습니다.
> 반드시 `env:`를 거쳐 `$VAR`로 참조하세요. 이것이 실무 표준입니다.

### ⌨️ 할 일

`github.` 컨텍스트를 쓰는 표현식을 최소 하나 넣으세요.

<details><summary>정답 보기</summary>

```yaml
      - name: Run fortune
        run: python scripts/fortune.py
        env:
          FORTUNE_FOR: ${{ github.actor }}
```
</details>
