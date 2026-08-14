"""
data.json 로드 및 스키마 검증 모듈.

이 모듈은 다음 역할을 담당한다.
- data.json 파일을 읽어 dict로 변환
- filters(size_5, size_13, size_25)를 {size: {"Cross": .., "X": ..}} 형태로 파싱
- patterns(size_{N}_{idx})를 파싱하고, 키에서 N을 추출
- 필터/패턴 크기 불일치 등 스키마 오류를 검증
  (오류가 있어도 프로그램이 중단되지 않고, 케이스 단위로 FAIL 처리할 수 있도록
   검증 결과만 반환한다)
"""

import json
import re

from modules.label_normalizer import normalize_label
from modules.matrix_utils import is_square

_SIZE_KEY_RE = re.compile(r"size_(\d+)")
_PATTERN_KEY_RE = re.compile(r"size_(\d+)_(\w+)")


def load_json(path):
    """data.json 파일을 읽어 dict로 반환한다."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_filters(raw_data):
    """
    raw_data["filters"]를 파싱하여
    {size(int): {"Cross": matrix, "X": matrix}} 형태로 반환한다.
    filter 키('cross', 'x')는 표준 라벨로 정규화한다.
    """
    filters = {}
    raw_filters = raw_data.get("filters", {})

    for size_key, label_dict in raw_filters.items():
        match = _SIZE_KEY_RE.match(size_key)
        if not match:
            continue
        size = int(match.group(1))

        normalized_labels = {}
        for raw_label, matrix in label_dict.items():
            std_label = normalize_label(raw_label)
            if std_label is None:
                continue
            normalized_labels[std_label] = matrix

        filters[size] = normalized_labels

    return filters


def parse_patterns(raw_data):
    """
    raw_data["patterns"]를 파싱하여
    [{"case_id", "size", "input", "expected"}, ...] 리스트로 반환한다.
    - 키(size_{N}_{idx})에서 N을 추출하여 "size"에 저장한다.
    - expected 값('+', 'x')은 표준 라벨(Cross/X)로 정규화한다.
    """
    patterns = []
    raw_patterns = raw_data.get("patterns", {})

    for case_id, case in raw_patterns.items():
        match = _PATTERN_KEY_RE.match(case_id)
        size = int(match.group(1)) if match else None

        patterns.append({
            "case_id": case_id,
            "size": size,
            "input": case.get("input"),
            "expected": normalize_label(case.get("expected")),
        })

    return patterns


def validate_case(case, filters):
    """
    패턴 케이스 하나를 검증한다.
    문제가 있으면 (False, 사유), 정상이면 (True, None)을 반환한다.
    이 함수는 예외를 던지지 않으므로, 호출부에서 케이스 단위 FAIL 처리를 할 수 있다.
    """
    if case["size"] is None:
        return False, f"케이스 키({case['case_id']})에서 크기(N)를 추출할 수 없습니다."

    if case["size"] not in filters:
        return False, f"size_{case['size']}에 해당하는 필터가 존재하지 않습니다."

    size_filters = filters[case["size"]]
    if "Cross" not in size_filters or "X" not in size_filters:
        return False, f"size_{case['size']} 필터에 Cross/X 라벨이 모두 존재하지 않습니다."

    if case["expected"] is None:
        return False, "expected 값을 정규화할 수 없습니다 (알 수 없는 라벨)."

    pattern = case["input"]
    if pattern is None or not is_square(pattern):
        return False, "패턴이 존재하지 않거나 정사각(N x N) 형태가 아닙니다."

    if len(pattern) != case["size"]:
        return (
            False,
            f"필터 크기(size_{case['size']})와 패턴 크기({len(pattern)})가 일치하지 않습니다.",
        )

    return True, None