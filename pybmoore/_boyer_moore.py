from collections import deque
from functools import singledispatch
from typing import Dict, List, Tuple


@singledispatch
def search(pattern: List[str], source: str) -> Dict:
    return {criteria: search(criteria, source) for criteria in pattern}


@search.register(str)  # type: ignore
def _(pattern: str, source: str) -> List[Tuple[int, int]]:
    pattern_len = len(pattern)
    good_suffix = suffix_shift(pattern)
    bad_char = bad_char_shift(pattern)
    source_len = len(source)
    r = []
    i = 0
    while i < ((source_len - pattern_len) + 1):
        sliding_window = pattern_len
        while (
            sliding_window > 0
            and pattern[sliding_window - 1] == source[i + sliding_window - 1]
        ):
            sliding_window -= 1
        if sliding_window > 0:
            # badchar_shift = bad_char.get(source[i + sliding_window - 1], pattern_len)
            try:
                badchar_shift = bad_char[source[i + sliding_window - 1]]
            except KeyError:
                badchar_shift = pattern_len
            goodsuffix_shift = good_suffix[pattern_len - sliding_window]
            if badchar_shift > goodsuffix_shift:
                i += badchar_shift
            else:
                i += goodsuffix_shift
        else:
            r.append((i, i + pattern_len))
            i += 1
    return r


def bad_char_shift(pattern: str) -> Dict[str, int]:
    pattern_len = len(pattern) - 1
    return {pattern[i]: (pattern_len - i) for i in range(pattern_len)}


def suffix_shift(pattern: str) -> Dict:
    pattern_len = len(pattern)
    skip_list = {}
    _buffer: deque = deque()
    for badchar in pattern[::-1]:
        skip_list[len(_buffer)] = suffix_position(
            badchar, _buffer, pattern, pattern_len
        )
        _buffer.appendleft(badchar)
    return skip_list


def suffix_position(badchar: str, suffix: deque, pattern: str, pattern_len: int):
    suffix_len = len(suffix)
    for offset in range(1, pattern_len + 1)[::-1]:
        flag = True
        term_index = (offset - suffix_len) - 1
        for suffix_index in range(suffix_len):
            if (term_index > 0) or (
                suffix[suffix_index] != pattern[term_index + suffix_index]
            ):
                flag = False
        if flag and (term_index <= 0 or pattern[term_index - 1] != badchar):
            return pattern_len - offset + 1
