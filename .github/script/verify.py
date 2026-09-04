#!/usr/bin/env python3
"""학습자의 practice.yml을 현재 STEP 규칙으로 채점한다.

핵심 교육 포인트: YAML 문서는 파이썬 dict/list로 그대로 로드된다.
따라서 채점기는 정규식이 아니라 자료구조 탐색으로 작성되어 있다.
"""
from __future__ import annotations

import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
STEP_FILE = ROOT / ".github/script/STEP"
PRACTICE = ROOT / ".github/workflows/practice.yml"
LAST_STEP = 8


def load() -> dict:
    if not PRACTICE.exists():
        fail("`.github/workflows/practice.yml` 파일이 없습니다. 먼저 만들어 주세요.")
    text = PRACTICE.read_text(encoding="utf-8")
    if "\t" in text:
        fail("탭 문자가 있습니다. YAML은 들여쓰기에 탭을 금지합니다. 스페이스 2칸을 쓰세요.")
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as exc:  # 파싱 실패 = 파이썬 SyntaxError에 해당
        fail(f"YAML 파싱 실패:\n```\n{exc}\n```")
    if not isinstance(doc, dict):
        fail("최상위는 매핑(dict)이어야 합니다.")
    return doc


def triggers(doc: dict):
    """`on:`은 YAML 1.1에서 불리언 True로 파싱된다 — 두 키를 모두 확인."""
    return doc.get("on", doc.get(True))


def jobs(doc: dict) -> dict:
    j = doc.get("jobs")
    if not isinstance(j, dict) or not j:
        fail("`jobs:` 매핑에 job이 최소 1개 필요합니다.")
    return j


def first_job(doc: dict) -> dict:
    return next(iter(jobs(doc).values()))


def steps_of(job: dict) -> list:
    s = job.get("steps")
    if not isinstance(s, list):
        fail("job에 `steps:` 리스트가 필요합니다. 각 항목은 `-`로 시작합니다.")
    return s


def flat_text(node) -> str:
    """중첩 구조 전체를 문자열로 펼친다 (표현식 탐색용)."""
    return yaml.safe_dump(node, allow_unicode=True, default_flow_style=False)


def fail(msg: str) -> None:
    print(f"::error::{msg}")
    pathlib.Path("result.md").write_text(f"### ❌ 아직입니다\n\n{msg}\n", encoding="utf-8")
    sys.exit(1)


# --- 단계별 규칙 ------------------------------------------------------------

def step1(doc):
    if "name" not in doc:
        fail("워크플로 최상위에 `name:`이 없습니다.")
    if triggers(doc) is None:
        fail("`on:` 트리거가 없습니다.")
    job = first_job(doc)
    if "runs-on" not in job:
        fail("job에 `runs-on:`이 없습니다. 예: `runs-on: ubuntu-latest`")


def step2(doc):
    s = steps_of(first_job(doc))
    if len(s) < 2:
        fail(f"step이 {len(s)}개입니다. `-` 항목을 2개 이상 만드세요.")
    if not any(isinstance(x, dict) and "name" in x for x in s):
        fail("step 중 최소 하나에 `name:`을 붙여 주세요.")


def step3(doc):
    s = steps_of(first_job(doc))
    uses = [x.get("uses", "") for x in s if isinstance(x, dict)]
    if not any(u.startswith("actions/checkout@") for u in uses):
        fail("`actions/checkout@v5` step이 필요합니다.")
    if not any(u.startswith("actions/setup-python@") for u in uses):
        fail("`actions/setup-python@v5` step이 필요합니다.")
    if any(u and "@" not in u for u in uses):
        fail("모든 `uses:`에 버전을 고정하세요. 예: `actions/checkout@v5`")
    if not any(isinstance(x, dict) and "run" in x for x in s):
        fail("`run:` step이 최소 1개 필요합니다.")


def step4(doc):
    s = steps_of(first_job(doc))
    runs = [x["run"] for x in s if isinstance(x, dict) and "run" in x]
    if not any("\n" in r.strip() for r in runs):
        fail("블록 스칼라 `|`로 여러 줄 `run:`을 하나 만드세요.")
    if not any("fortune.py" in r for r in runs):
        fail("`python scripts/fortune.py`를 실행하는 줄이 필요합니다.")
    for x in s:
        if isinstance(x, dict) and isinstance(x.get("with"), dict):
            v = x["with"].get("python-version")
            if v is not None and not isinstance(v, str):
                fail(f"`python-version: {v}`가 문자열이 아닙니다. 따옴표로 감싸세요: \"3.12\"")


def step5(doc):
    job = first_job(doc)
    s = steps_of(job)
    envs = [job.get("env")] + [x.get("env") for x in s if isinstance(x, dict)]
    merged = {k: v for e in envs if isinstance(e, dict) for k, v in e.items()}
    if "FORTUNE_FOR" not in merged:
        fail("`env:`로 `FORTUNE_FOR` 환경변수를 정의하세요 (job 또는 step 레벨).")


def step6(doc):
    text = flat_text(doc)
    if "${{" not in text:
        fail("`${{ }}` 표현식을 아직 쓰지 않았습니다.")
    if "github." not in text:
        fail("`github.` 컨텍스트를 사용하세요. 예: ${{ github.actor }}")


def step7(doc):
    js = jobs(doc)
    if len(js) < 2:
        fail("job이 2개 필요합니다. 두 번째 job에서 첫 job의 출력을 받습니다.")
    if not any("needs" in j for j in js.values()):
        fail("두 번째 job에 `needs:`를 추가하세요.")
    if not any(isinstance(j.get("outputs"), dict) for j in js.values()):
        fail("첫 job에 `outputs:`를 정의하세요 (`steps.<id>.outputs.<key>` 참조).")
    text = flat_text(doc)
    if "steps." not in text or ".outputs." not in text:
        fail("`steps.<id>.outputs.<key>` 형태의 참조가 필요합니다. step에 `id:`를 붙였나요?")
    if "if:" not in PRACTICE.read_text(encoding="utf-8"):
        fail("`if:` 조건을 최소 한 곳에 넣어 주세요.")


def step8(doc):
    js = jobs(doc)
    matrix = None
    for j in js.values():
        strategy = j.get("strategy")
        if isinstance(strategy, dict) and isinstance(strategy.get("matrix"), dict):
            matrix = strategy["matrix"]
    if matrix is None:
        fail("`strategy: matrix:`가 없습니다.")
    combos = 1
    for v in matrix.values():
        if isinstance(v, list):
            combos *= len(v)
    if combos < 3:
        fail(f"매트릭스 조합이 {combos}개입니다. 3개 이상이 되게 값을 늘리세요.")
    if "permissions" not in doc and not any("permissions" in j for j in js.values()):
        fail("`permissions:`를 명시해 최소 권한을 선언하세요.")


RULES = {1: step1, 2: step2, 3: step3, 4: step4, 5: step5, 6: step6, 7: step7, 8: step8}


def main() -> None:
    step = int(STEP_FILE.read_text().strip() or 0)
    if step < 1 or step > LAST_STEP:
        print(f"채점 대상 단계 아님 (STEP={step}). 종료.")
        return
    doc = load()
    RULES[step](doc)
    print(f"::notice::Step {step} 통과")
    STEP_FILE.write_text(f"{step + 1}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
