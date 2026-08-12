# utils.py - 패턴 판별 구현

from models import Array2D

def is_diagonal(matrix):
    """
    대각선 패턴 확인
    - 대각선(i == j) 위치는 0이 아니어야 함
    - 나머지 위치는 모두 0이어야 함
    """
    rows, cols = matrix.size()

    # 정사각형 행렬만 대각선 패턴 가능
    if rows != cols:
        return False

    for i in range(rows):
        for j in range(cols):
            if i == j:
                if matrix.get(i, j) == 0:   # 대각선이 0이면 탈락
                    return False
            else:
                if matrix.get(i, j) != 0:   # 대각선 외가 0이 아니면 탈락
                    return False
    return True


def is_cross(matrix):
    """
    십자가 패턴 확인
    - 중앙 행/열 위치는 0이 아니어야 함
    - 나머지 위치는 모두 0이어야 함
    """
    rows, cols = matrix.size()

    # 홀수 크기만 십자가 패턴 가능 (중앙이 명확해야 함)
    if rows % 2 == 0 or cols % 2 == 0:
        return False

    mid_r = rows // 2  # 중앙 행
    mid_c = cols // 2  # 중앙 열

    for i in range(rows):
        for j in range(cols):
            is_center = (i == mid_r or j == mid_c)  # 중앙 행 or 중앙 열
            if is_center:
                if matrix.get(i, j) == 0:   # 중앙 행/열이 0이면 탈락
                    return False
            else:
                if matrix.get(i, j) != 0:   # 나머지가 0이 아니면 탈락
                    return False
    return True


def classify_pattern(matrix):
    """
    패턴 판별 후 문자열 반환
    반환값: 'diagonal' / 'cross' / 'unknown'
    """
    if is_diagonal(matrix):
        return 'diagonal'
    elif is_cross(matrix):
        return 'cross'
    else:
        return 'unknown'