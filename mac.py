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
    n2, p = B.size()

    # 행렬 크기 검증
    if n != n2:
        raise ValueError(f"행렬 크기 불일치: A의 열({n}) ≠ B의 행({n2})")

    # 결과 행렬 초기화 (0으로 채움)
    result = Array2D([[0] * p for _ in range(m)])

    # 3중 for문 MAC 연산
    for i in range(m):
        for j in range(p):
            acc = 0                          # accumulator 초기화
            for k in range(n):
                acc += A.get(i, k) * B.get(k, j)  # Multiply + Accumulate
            result.set(i, j, acc)

    return result