# OUTLINE — 실습 설계 문서

이 문서는 강사/기여자용입니다. 학습자는 README와 이슈만 보면 됩니다.

## 1. 설계 원칙

| 원칙 | 적용 |
|---|---|
| 뿌리부터 | YAML 문법 → Actions 스키마 순서. 1~4단계는 순수 YAML, 5~8단계는 Actions 고유 문법 |
| 파이썬 앵커 | 모든 문법을 파이썬 자료구조에 1:1 대응시켜 설명 |
| 자기검증 | 채점기 자체가 PyYAML 파이썬 코드 → 학습자가 채점 로직을 읽으며 또 배움 |
| 하나의 산출물 | 8단계 내내 `practice.yml` 한 파일을 키워나감 (버리는 코드 없음) |

## 2. YAML ↔ 파이썬 대응표 (실습의 뼈대)

| YAML | 파이썬 | 실습 단계 |
|---|---|---|
| `key: value` | `{"key": "value"}` (dict) | 1 |
| 들여쓰기 2칸 (탭 금지) | 중첩 dict | 1 |
| `- item` | `["item"]` (list) | 2 |
| `- key: v` | `[{"key": "v"}]` (list of dict) | 2 |
| `\|` 블록 (개행 유지) | `"a\nb\n"` | 4 |
| `>` 폴디드 (개행→공백) | `"a b\n"` | 4 |
| `"3.10"` vs `3.10` | `str` vs `float` → **파이썬 3.1 사고** | 4 |
| `&anchor` / `*alias` | 같은 객체 참조 (`a = b`) | 8 |
| `${{ }}` | f-string / 템플릿 치환 | 6 |

> [!WARNING]
> **유명한 함정**: PyYAML(YAML 1.1)은 `on:` 을 불리언 `True`로 파싱합니다.
> `yaml.safe_load(...)["on"]` 이 `KeyError`를 내는 이유이고, 채점기는 `True` 키도 함께 조회합니다.
> `yes/no/off`도 같은 이유로 불리언이 됩니다. 버전 번호 `3.10`이 float가 되는 것과 같은 계열의 사고입니다.

## 3. 단계 구성

| # | 단계 파일 | 핵심 문법 | 통과 조건 (verify.py) |
|---|---|---|---|
| 1 | `1-mapping.md` | 매핑, 들여쓰기, 주석, `name`/`on`/`jobs` | 파싱 성공 + 3대 키 존재 + job에 `runs-on` |
| 2 | `2-sequence.md` | 시퀀스 `-`, step 매핑, `name` | `steps` 길이 ≥ 2 |
| 3 | `3-run-uses.md` | `run` vs `uses`, `@v5` 버전 고정 | checkout(핀) + setup-python + run 각 1개 |
| 4 | `4-scalars.md` | `\|`, `>`, 따옴표, 버전 문자열 | 멀티라인 run + `python-version`이 문자열 |
| 5 | `5-env-with.md` | `env`, `with`, 스코프 | step/job `env` 존재 + 값이 로그에 출력 |
| 6 | `6-expressions.md` | `${{ }}`, `github.*`, `secrets.*` | 표현식에 `github.` 컨텍스트 사용 |
| 7 | `7-outputs.md` | `id`, `outputs`, `needs`, `if` | job 2개 + `needs` + `steps.<id>.outputs` |
| 8 | `8-matrix.md` | `strategy.matrix`, `permissions`, 앵커 | matrix 조합 ≥ 3 + `permissions` 명시 |
| x | `x-review.md` | 회고 + 다음 학습 | — |

## 4. 자동화 흐름

```
학습자 push (main)
   └─> .github/workflows/check-step.yml  (on: push)
         ├─ actions/checkout@v5
         ├─ actions/setup-python@v5  + pip install pyyaml
         ├─ python .github/script/verify.py   ← 현재 STEP 규칙으로 practice.yml 채점
         │     ├─ 실패: 이슈에 힌트 코멘트, STEP 유지, 워크플로 실패
         │     └─ 성공: STEP += 1
         └─ 성공 시 다음 .github/steps/N-*.md 를 이슈 코멘트로 게시 + STEP 커밋
```

- 상태 저장: `.github/script/STEP` (한 줄 정수). 파이썬으로 읽고 쓰기 때문에 별도 액션 불필요.
- 게시 수단: `gh issue comment`(GitHub CLI는 러너에 기본 설치) + `GITHUB_TOKEN`.
- 권한: `permissions: { contents: write, issues: write }` — 8단계에서 배울 개념을 채점기가 먼저 시범 보임.

## 5. 파일 트리

```
.
├── README.md                     학습자 랜딩
├── OUTLINE.md                    이 문서
├── scripts/fortune.py            학습자가 워크플로에서 실행할 파이썬 스크립트
└── .github/
    ├── script/
    │   ├── STEP                  현재 단계 (초기값 0)
    │   └── verify.py             PyYAML 채점기 + 단계별 규칙
    ├── steps/1-mapping.md … x-review.md
    └── workflows/
        ├── 0-start-exercise.yml  템플릿 복사 직후 1회 실행, 추적 이슈 생성
        ├── check-step.yml        매 push마다 채점
        └── practice.yml          ← 학습자가 편집하는 유일한 파일 (1단계에서 생성)
```

## 6. 커스터마이즈 포인트

- 난이도를 낮추려면 7단계를 `needs`만 남기고 `outputs`를 9단계로 분리하세요 (10단계 버전).
- 사내 교육이면 8단계 matrix를 파이썬 버전 대신 `os: [ubuntu-latest, windows-latest]`로 바꿔 러너 차이를 체감시키면 좋습니다.
- 공식 GitHub Skills 스타일로 배포하려면 `check-step.yml`을 `skills/exercise-toolkit` 재사용 워크플로 호출로 교체하면 됩니다.

## 7. 정답 참조

`solution/practice-final.yml`은 8단계까지 모두 통과하는 최종본입니다. 배포 전 채점기 회귀 테스트에 쓰세요.
