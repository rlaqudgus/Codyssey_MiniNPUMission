"""
크기별 MAC 연산 성능(시간) 측정 모듈.

각 크기(N x N)에 대해 MAC 연산을 여러 번 반복 실행하고
평균 소요 시간(ms)을 측정한다. 입력/출력(I/O) 시간은 제외하고
"연산 함수 호출 구간"만 시간을 잰다.
"""

import time

from modules.mac_engine import mac_score

DEFAULT_REPEAT = 10


def measure_mac_time_ms(pattern, filter_matrix, repeat=DEFAULT_REPEAT):
    """
    MAC 연산을 repeat회 반복 실행하여 평균 소요 시간(ms)을 측정해 반환한다.
    """
    start = time.perf_counter()
    for _ in range(repeat):
        mac_score(pattern, filter_matrix)
    end = time.perf_counter()

    total_ms = (end - start) * 1000
    return total_ms / repeat


def build_performance_table(size_to_matrices, repeat=DEFAULT_REPEAT):
    """
    {size: (pattern, filter)} 형태의 입력을 받아
    크기 오름차순으로 [(size, 평균시간ms, 연산횟수 N^2), ...] 리스트를 반환한다.
    """
    results = []
    for size in sorted(size_to_matrices.keys()):
        pattern, filter_matrix = size_to_matrices[size]
        avg_ms = measure_mac_time_ms(pattern, filter_matrix, repeat)
        results.append((size, avg_ms, size * size))
    return results