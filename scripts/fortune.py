"""Octo-Fortune: 오늘의 운세를 한 줄 출력한다."""
import os
import random

FORTUNES = [
    "오늘의 빌드는 한 번에 통과합니다. 🍀",
    "머지 컨플릭트가 당신을 피해 갑니다.",
    "누군가 당신의 PR을 30초 안에 승인합니다.",
    "탭 대신 스페이스를 쓰면 행운이 따릅니다.",
    "캐시가 히트합니다. 오늘은 그런 날입니다.",
]


def main() -> None:
    name = os.getenv("FORTUNE_FOR", "Octocat")
    print(f"{name}님의 운세: {random.choice(FORTUNES)}")


if __name__ == "__main__":
    main()
