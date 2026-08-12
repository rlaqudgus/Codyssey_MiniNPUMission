# mac.py - 핵심 MAC 연산 구현

from models import Array2D

def mac_multiply(A, B):
    """
    행렬 A × B를 MAC 연산으로 계산
    A: Array2D (m × n)
    B: Array2D (n × p)
    반환: Array2D (m × p)
    """
    m, n = A.size()

    # 결과 행렬 초기화
    result = Array2D([[0] * n for _ in range(m)])

    # element-wise MAC 연산 (같은 자리끼리 곱셈)
    for i in range(m):
        for j in range(n):
            result.set(i, j, A.get(i, j) * B.get(i, j))  # 같은 [i][j]끼리!

    return result