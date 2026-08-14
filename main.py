"""
Mini NPU Simulator
==================
MAC(Multiply-Accumulate) 연산으로 패턴(십자가/X)을 판별하는
Mini NPU 시뮬레이터 콘솔 애플리케이션.

실행 방법:
    python main.py

이 파일은 각 기능 모듈(modules/*)을 불러와 실행 흐름만 조율한다.
실제 로직(입력/검증/연산/성능측정/출력)은 각 모듈이 담당한다.
"""

import os

from modules.input_handler import read_matrix
from modules.mac_engine import mac_score, judge
from modules.performance import measure_mac_time_ms, build_performance_table, DEFAULT_REPEAT
from modules.data_loader import load_json, parse_filters, parse_patterns, validate_case
from modules import report

DATA_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

# 성능 분석(3x3)용 기본 예시 패턴 - 미션 소개에 등장하는 예시와 동일하다.
BASE_3X3_CROSS = [
    [0.0, 1.0, 0.0],
    [1.0, 1.0, 1.0],
    [0.0, 1.0, 0.0],
]
BASE_3X3_X = [
    [1.0, 0.0, 1.0],
    [0.0, 1.0, 0.0],
    [1.0, 0.0, 1.0],
]


def _process_pattern_case(case, filters):
    """
    패턴 케이스 하나를 검증 -> MAC 연산 -> 판정까지 처리하고, 결과를 즉시 출력한다.
    반환값: (is_pass: bool, fail_reason: str | None)
    fail_reason은 통과한 경우 None이다.
    """
    is_valid, reason = validate_case(case, filters)
    if not is_valid:
        report.print_case_error(case["case_id"], reason)
        return False, reason

    size = case["size"]
    pattern = case["input"]
    expected = case["expected"]

    cross_score = mac_score(pattern, filters[size]["Cross"])
    x_score = mac_score(pattern, filters[size]["X"])
    verdict = judge(cross_score, x_score, "Cross", "X")

    is_pass = (verdict == expected)
    report.print_case_result(case["case_id"], cross_score, x_score, verdict, expected, is_pass)

    if is_pass:
        return True, None
    if verdict == "UNDECIDED":
        return False, "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
    return False, f"판정({verdict})이 expected({expected})와 다름"


def _build_performance_inputs(filters):
    """
    성능 분석에 사용할 {크기: (Cross 필터, X 필터)} 딕셔너리를 만든다.
    기본 3x3 예시에 더해, data.json에 존재하는 모든 크기를 포함한다.
    """
    perf_inputs = {3: (BASE_3X3_CROSS, BASE_3X3_X)}
    for size, size_filters in filters.items():
        if "Cross" in size_filters and "X" in size_filters:
            perf_inputs[size] = (size_filters["Cross"], size_filters["X"])
    return perf_inputs


def run_mode1():
    """
    모드 1: 사용자 입력(3x3)
    필터 A, B 입력 -> 저장 확인 -> 패턴 입력 -> MAC 연산 -> 판정 -> 성능 분석 순으로 진행한다.
    """
    report.print_header("[1] 필터 입력")
    filter_a = read_matrix("필터 A")
    filter_b = read_matrix("필터 B")
    print("\n저장 완료: 필터 A, 필터 B")

    report.print_header("[2] 패턴 입력")
    pattern = read_matrix("패턴")

    score_a = mac_score(pattern, filter_a)
    score_b = mac_score(pattern, filter_b)
    verdict = judge(score_a, score_b, "A", "B")

    avg_ms = measure_mac_time_ms(pattern, filter_a, DEFAULT_REPEAT)

    report.print_header("[3] MAC 결과")
    report.print_mode1_result(score_a, score_b, verdict, avg_ms)


def run_mode2():
    """
    모드 2: data.json 분석
    필터 로드 -> 패턴 로드/검증 -> MAC 연산/판정/PASS-FAIL 출력
    -> 성능 분석(3x3, 5x5, 13x13, 25x25) -> 결과 요약 순으로 진행한다.
    """
    try:
        raw_data = load_json(DATA_JSON_PATH)
    except (FileNotFoundError, ValueError, OSError) as e:
        print(f"data.json을 읽는 중 오류가 발생했습니다: {e}")
        return

    filters = parse_filters(raw_data)
    patterns = parse_patterns(raw_data)

    report.print_header("[1] 필터 로드")
    report.print_filter_load_status(filters)

    report.print_header("[2] 패턴 분석 (라벨 정규화 적용)")

    fail_cases = []
    passed = 0

    for case in patterns:
        is_pass, fail_reason = _process_pattern_case(case, filters)
        if is_pass:
            passed += 1
        else:
            fail_cases.append((case["case_id"], fail_reason))

    total = len(patterns)
    failed = total - passed

    results = build_performance_table(_build_performance_inputs(filters), DEFAULT_REPEAT)

    report.print_header("[3] 성능 분석 (평균/10회)")
    report.print_performance_table(results)

    report.print_header("[4] 결과 요약")
    report.print_summary(total, passed, failed, fail_cases)


def select_mode():
    """모드 선택 메뉴를 출력하고, 유효한 선택("1" 또는 "2")을 받을 때까지 반복한다."""
    print("=== Mini NPU Simulator ===")
    print("\n[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    while True:
        choice = input("선택: ").strip()
        if choice in ("1", "2"):
            return choice
        print("잘못된 입력입니다. 1 또는 2를 입력하세요.")


def main():
    """프로그램 진입점: 모드를 선택받아 해당 흐름을 실행한다."""
    choice = select_mode()
    if choice == "1":
        run_mode1()
    else:
        run_mode2()


if __name__ == "__main__":
    main()