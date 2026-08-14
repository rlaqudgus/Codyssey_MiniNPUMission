"""
MAC(Multiply-Accumulate) 연산 엔진.

패턴과 필터를 같은 위치끼리 곱한 뒤 모두 더하는(MAC) 연산을
NumPy 등 외부 라이브러리 없이 순수 반복문으로 구현한다.

또한 두 점수(예: Cross 점수 vs X 점수)를 비교하여 판정하는
기능도 함께 제공한다. 부동소수점 오차를 고려해
허용오차(epsilon) 기반으로 동점 여부를 판단한다.
"""

EPSILON = 1e-9


def mac_score(pattern, filter_matrix):
    """
    패턴과 필터를 위치별로 곱하고(Multiply), 그 결과를 모두 더한다(Accumulate).
    두 행렬의 크기가 다르면 ValueError를 발생시킨다.
    """
    rows = len(pattern)
    if rows == 0 or rows != len(filter_matrix):
        raise ValueError("패턴과 필터의 행 수가 일치하지 않습니다.")

    total = 0.0
    for r in range(rows):
        pattern_row = pattern[r]
        filter_row = filter_matrix[r]

        if len(pattern_row) != len(filter_row):
            raise ValueError("패턴과 필터의 열 수가 일치하지 않습니다.")

        for c in range(len(pattern_row)):
            total += pattern_row[c] * filter_row[c]

    return total


def judge(score_a, score_b, label_a="A", label_b="B", epsilon=EPSILON):
    """
    두 점수를 허용오차(epsilon) 기반으로 비교하여 판정 라벨을 반환한다.
    |score_a - score_b| < epsilon 이면 동점으로 간주하여 'UNDECIDED'를 반환한다.
    """
    if abs(score_a - score_b) < epsilon:
        return "UNDECIDED"
    return label_a if score_a > score_b else label_b