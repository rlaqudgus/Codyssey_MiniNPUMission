"""
모드 1(사용자 입력, 3x3) 콘솔 입출력 처리 모듈.

필터 A, 필터 B, 패턴을 "한 줄씩(공백 구분)" 입력받고,
행/열 개수 불일치나 숫자 파싱 실패 시 안내 문구를 출력한 뒤
재입력을 유도한다.
"""

from modules.matrix_utils import is_square

DEFAULT_SIZE = 3


def _parse_line(line):
    """공백으로 구분된 한 줄의 문자열을 float 리스트로 변환한다. 실패 시 None을 반환한다."""
    tokens = line.strip().split()
    try:
        return [float(t) for t in tokens]
    except ValueError:
        return None


def read_matrix(prompt_title, size=DEFAULT_SIZE):
    """
    size x size 크기의 행렬을 size줄에 걸쳐 공백 구분으로 입력받는다.
    형식 오류가 발생하면 안내 문구를 출력하고 처음부터 다시 입력받는다.
    """
    print(f"\n{prompt_title} ({size}줄 입력, 공백 구분)")

    while True:
        matrix = []
        error_message = None

        for _ in range(size):
            line = input()
            values = _parse_line(line)

            if values is None or len(values) != size:
                error_message = (
                    f"입력 형식 오류: 각 줄에 {size}개의 숫자를 "
                    f"공백으로 구분해 입력하세요."
                )
                break

            matrix.append(values)

        if error_message is not None:
            print(error_message)
            print(f"{prompt_title} 다시 입력해주세요 ({size}줄, 공백 구분)")
            continue

        if not is_square(matrix):
            print(f"입력 형식 오류: {size}x{size} 정사각 행렬이어야 합니다.")
            print(f"{prompt_title} 다시 입력해주세요 ({size}줄, 공백 구분)")
            continue

        return matrix


def read_mode1_inputs(size=DEFAULT_SIZE):
    """필터 A, 필터 B, 패턴을 순서대로 입력받아 (filter_a, filter_b, pattern)으로 반환한다."""
    filter_a = read_matrix("필터 A", size)
    filter_b = read_matrix("필터 B", size)
    pattern = read_matrix("패턴", size)
    return filter_a, filter_b, pattern