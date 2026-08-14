"""
콘솔 결과 출력(리포트) 모듈.

MAC 연산 결과, 필터 로드 상태, 패턴 판정 결과, 성능 분석 표,
최종 요약 등 모든 "화면 출력"을 이 모듈이 전담한다.
연산/검증 로직과 출력 로직을 분리해 어떤 코드가 어떤 일을
하는지 명확히 구분하기 위함이다.
"""


def print_header(title):
    """섹션 구분용 헤더를 출력한다."""
    print("\n" + "-" * 40)
    print(f"# {title}")
    print("-" * 40)


def print_mode1_result(score_a, score_b, verdict, avg_ms):
    """모드 1(3x3 사용자 입력)의 MAC 결과를 출력한다."""
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/{10}회): {avg_ms:.3f} ms")

    if verdict == "UNDECIDED":
        print("판정: 판정 불가 (|A-B| < 1e-9)")
    else:
        print(f"판정: {verdict}")


def print_filter_load_status(filters):
    """data.json에서 로드된 필터들의 상태를 출력한다."""
    for size in sorted(filters.keys()):
        labels = ", ".join(sorted(filters[size].keys()))
        print(f"✓ size_{size} 필터 로드 완료 ({labels})")


def print_case_result(case_id, cross_score, x_score, verdict, expected, passed):
    """패턴 케이스 하나의 판정 결과를 출력한다."""
    print(f"\n--- {case_id} ---")
    print(f"Cross 점수: {cross_score}")
    print(f"X 점수: {x_score}")
    result = "PASS" if passed else "FAIL"
    print(f"판정: {verdict} | expected: {expected} | {result}")


def print_case_error(case_id, reason):
    """스키마/크기 검증에 실패한 케이스를 출력한다."""
    print(f"\n--- {case_id} ---")
    print(f"FAIL (검증 오류): {reason}")


def print_performance_table(results):
    """크기별 평균 연산 시간(ms)과 연산 횟수(N^2) 표를 출력한다."""
    print(f"{'크기':<10}{'평균 시간(ms)':<18}{'연산 횟수':<10}")
    print("-" * 40)
    for size, avg_ms, op_count in results:
        label = f"{size}x{size}"
        print(f"{label:<10}{avg_ms:<18.3f}{op_count:<10}")


def print_summary(total, passed, failed, fail_cases):
    """전체 테스트 수/통과 수/실패 수 및 실패 케이스 목록을 출력한다."""
    print(f"총 테스트: {total}개")
    print(f"통과: {passed}개")
    print(f"실패: {failed}개")

    if fail_cases:
        print("\n실패 케이스:")
        for case_id, reason in fail_cases:
            print(f"- {case_id}: {reason}")