## Step 8: `matrix`와 `permissions` — 확장과 방어

**matrix**: 같은 job을 값 조합만큼 복제해 병렬 실행합니다. 파이썬의 `itertools.product`와 같습니다.

```yaml
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12", "3.13"]   # 3개 job 동시 실행
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

**permissions**: `GITHUB_TOKEN`의 권한 범위입니다. 명시하지 않으면 레포 기본값을 상속합니다. 최소 권한 원칙에 따라 필요한 것만 켜세요.

```yaml
permissions:
  contents: read
  pull-requests: write
```

**앵커(anchor)** — 중복 제거용 YAML 기본 문법. `&`로 정의하고 `*`로 재사용하며, 파이썬에서 같은 객체를 두 변수에 대입하는 것과 같습니다.

```yaml
x-defaults: &py "3.12"
# 이후 python-version: *py
```
(단, Actions는 앵커를 파일 하나 안에서만 해석합니다.)

### ⌨️ 할 일

첫 job에 `strategy.matrix`로 파이썬 버전 3개를 돌리고, 워크플로 최상단에 `permissions:`를 선언하세요.
