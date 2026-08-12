# modes.py - 모드 선택 및 실행 로직

import json
from models import Array2D
from mac import matrix_multiply
from utils import classify_pattern


def input_matrix(name):
    """
    터미널에서 행렬 직접 입력받기
    name: 행렬 이름 (예: 'A', 'B')
    """
    print(f"\n[ 행렬 {name} 입력 ]")
    rows = int(input("  행 수 입력: "))
    cols = int(input("  열 수 입력: "))

    matrix = Array2D(rows, cols)

    print(f"  {rows}x{cols} 행렬 값을 입력하세요 (행 단위, 공백 구분)")
    for i in range(rows):
        row_data = list(map(int, input(f"  {i+1}행: ").split()))
        for j in range(cols):
            matrix[i][j] = row_data[j]

    return matrix


def print_matrix(name, matrix):
    """
    행렬 출력
    name: 행렬 이름
    matrix: Array2D 객체
    """
    rows, cols = matrix.size()
    print(f"\n[ 행렬 {name} ]")
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(str(matrix[i][j]))
        print("  " + " ".join(row))


def print_result(A, B, C, pattern):
    """
    입력 행렬 / 결과 행렬 / 패턴 출력
    """
    print_matrix("A", A)
    print_matrix("B", B)
    print_matrix("결과 (A x B)", C)
    print(f"\n[ 패턴 판별 결과 ] → {pattern}")


def mode1():
    """
    모드 1: 터미널 직접 입력
    """
    print("\n========== MODE 1: 직접 입력 ==========")

    A = input_matrix("A")
    B = input_matrix("B")

    # 행렬 크기 검증 (A의 열 수 == B의 행 수)
    a_rows, a_cols = A.size()
    b_rows, b_cols = B.size()

    if a_cols != b_rows:
        print(f"\n❌ 오류: A의 열({a_cols}) != B의 행({b_rows}) → 곱셈 불가")
        return

    # 행렬 곱셈 + 패턴 판별
    C = matrix_multiply(A, B)
    pattern = classify_pattern(A)

    print_result(A, B, C, pattern)
    print("\n✅ 완료!")


def mode2():
    """
    모드 2: data.json 자동 테스트
    """
    print("\n========== MODE 2: 자동 테스트 ==========")

    # json 파일 읽기
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    test_cases = data["test_cases"]
    pass_count = 0

    for tc in test_cases:
        print(f"\n--- 테스트 {tc['id']}: {tc['description']} ---")

        # 리스트 → Array2D 변환
        raw_A = tc["A"]
        raw_B = tc["B"]

        rows_A, cols_A = len(raw_A), len(raw_A[0])
        rows_B, cols_B = len(raw_B), len(raw_B[0])

        A = Array2D(rows_A, cols_A)
        B = Array2D(rows_B, cols_B)

        for i in range(rows_A):
            for j in range(cols_A):
                A[i][j] = raw_A[i][j]

        for i in range(rows_B):
            for j in range(cols_B):
                B[i][j] = raw_B[i][j]

        # 행렬 곱셈 + 패턴 판별
        C = matrix_multiply(A, B)
        pattern = classify_pattern(A)
        expected = tc["expected_pattern"]

        print_result(A, B, C, pattern)

        # 패턴 정답 확인
        if pattern == expected:
            print(f"✅ PASS (예상: {expected} / 결과: {pattern})")
            pass_count += 1
        else:
            print(f"❌ FAIL (예상: {expected} / 결과: {pattern})")

    # 최종 결과
    print(f"\n========== 결과: {pass_count}/{len(test_cases)} 통과 ==========")