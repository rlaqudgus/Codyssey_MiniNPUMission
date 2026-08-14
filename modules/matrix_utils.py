"""
2차원 행렬(패턴/필터) 데이터를 다루는 유틸리티 모듈.

이 모듈은 다음 역할을 담당한다.
- n x n 크기의 행렬 생성
- 특정 위치(row, col)의 값 읽기/쓰기
- 행렬이 정사각형(N x N) 형태인지 검증
"""


def create_matrix(rows, cols, fill=0.0):
    """rows x cols 크기의 행렬을 fill 값으로 초기화하여 반환한다."""
    return [[fill for _ in range(cols)] for _ in range(rows)]


def get_value(matrix, row, col):
    """행렬의 특정 위치(row, col) 값을 읽어온다."""
    return matrix[row][col]


def set_value(matrix, row, col, value):
    """행렬의 특정 위치(row, col)에 값을 저장한다."""
    matrix[row][col] = value


def shape(matrix):
    """행렬의 (행 수, 열 수)를 반환한다. 열 수는 첫 번째 행 길이 기준이다."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    return rows, cols


def is_square(matrix):
    """
    행렬이 정사각형(N x N)이고, 모든 행의 길이가 서로 동일한지 검증한다.
    행렬이 비어 있거나 형태가 불규칙하면 False를 반환한다.
    """
    if not matrix:
        return False
    rows, cols = shape(matrix)
    if rows != cols:
        return False
    return all(len(row) == cols for row in matrix)