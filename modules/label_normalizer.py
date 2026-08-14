"""
라벨 정규화(표준화) 모듈.

data.json 안에는 같은 의미의 라벨이 서로 다른 표기로 등장한다.
    - filters 키:  'cross', 'x'
    - expected 값: '+', 'x'

이 모듈은 위 표기들을 프로그램 내부에서 사용하는
표준 라벨 두 가지, 'Cross' / 'X' 로 통일하는 역할을 한다.
표준 라벨로 통일해두면, 이후 모든 비교/출력 로직이
표기 차이를 신경 쓰지 않고 하나의 기준만 사용할 수 있다.
"""

STANDARD_LABELS = ("Cross", "X")

_LABEL_MAP = {
    "cross": "Cross",
    "+": "Cross",
    "x": "X",
}


def normalize_label(raw_label):
    """
    filter 키('cross', 'x') 또는 expected 값('+', 'x')을
    표준 라벨('Cross', 'X')로 변환한다.
    알 수 없는 표기이면 None을 반환한다.
    """
    if raw_label is None:
        return None
    key = str(raw_label).strip().lower()
    return _LABEL_MAP.get(key)