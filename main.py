# main.py - 프로그램 진입점

import time
from modes import mode1, mode2


def print_banner():
    """
    프로그램 시작 배너 출력
    """
    print("=" * 40)
    print("     Mini NPU 행렬곱셈 시뮬레이터")
    print("=" * 40)


def select_mode():
    """
    모드 선택 입력받기
    반환값: 1 또는 2
    """
    print("\n[ 모드 선택 ]")
    print("  1. 직접 입력 (터미널)")
    print("  2. 자동 테스트 (data.json)")

    while True:
        choice = input("\n모드를 선택하세요 (1 or 2): ").strip()
        if choice in ("1", "2"):
            return int(choice)
        print("❌ 1 또는 2만 입력 가능합니다. 다시 입력하세요.")


def main():
    """
    메인 함수 - 진입점
    """
    print_banner()

    mode = select_mode()

    # 실행 시간 측정 시작
    start = time.time()

    if mode == 1:
        mode1()
    elif mode == 2:
        mode2()

    # 실행 시간 측정 종료
    end = time.time()
    elapsed = end - start

    print(f"\n⏱️  실행 시간: {elapsed:.4f}초")
    print("=" * 40)
    print("     프로그램 종료")
    print("=" * 40)


if __name__ == "__main__":
    main()