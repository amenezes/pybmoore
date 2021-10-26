from collections import deque
from typing import Dict, List, Tuple

import cython


def search(pattern: str, source: str) -> List[Tuple[int, int]]:
    pattern_len: cython.int = len(pattern)
    source_len: cython.int = len(source)
    good_suffix = suffix_shift(pattern)
    bad_char = bad_char_shift(pattern)
    r = []
    i: cython.int = 0
    while i < ((source_len - pattern_len) + 1):
        sliding_window: cython.int = pattern_len
        while (
            sliding_window > 0
            and pattern[sliding_window - 1] == source[i + sliding_window - 1]
        ):
            sliding_window -= 1
        if sliding_window > 0:
            try:
                badchar_shift: cython.int = bad_char[source[i + sliding_window - 1]]
            except KeyError:
                badchar_shift: cython.int = pattern_len
            goodsuffix_shift = good_suffix[pattern_len - sliding_window]
            i += _calc_offset(badchar_shift, goodsuffix_shift)
        else:
            r.append((i, i + pattern_len))
            i += 1
    return r


@cython.cfunc
def _calc_offset(badchar_d: cython.int, goodsuffix_d: cython.int) -> cython.int:
    if badchar_d > goodsuffix_d:
        return badchar_d
    return goodsuffix_d


def bad_char_shift(pattern: str) -> Dict[str, int]:
    pattern_len: cython.int = len(pattern) - 1
    return {pattern[i]: (pattern_len - i) for i in range(pattern_len)}


def suffix_shift(pattern: str) -> Dict:
    pattern_len: cython.int = len(pattern)
    skip_list = {}
    _buffer: deque = deque()
    for badchar in pattern[::-1]:
        skip_list[len(_buffer)] = suffix_position(
            badchar, _buffer, pattern, pattern_len
        )

        _buffer.appendleft(badchar)
    return skip_list


def suffix_position(badchar: str, suffix: deque, pattern: str, pattern_len: int) -> int:
    suffix_len: cython.int = len(suffix)
    for offset in range(1, pattern_len + 1)[::-1]:
        flag: cython.uchar = 1
        term_index: cython.int = _term_index(offset, suffix_len)
        for suffix_index in range(suffix_len):
            flag: cython.uchar = _flag(
                term_index,
                suffix[suffix_index],
                pattern[term_index + suffix_index]
            )
        if flag and (term_index <= 0 or pattern[term_index - 1] != badchar):
            return pattern_len - offset + 1


@cython.cfunc
def _term_index(offset: cython.int, suffix_len: cython.int) -> cython.int:
    return (offset - suffix_len) - 1


@cython.cfunc
def _flag(term_index: cython.int, str suffix_char, str pattern_char) -> cython.uchar:
    if (term_index > 0) or (suffix_char != pattern_char):
        return 0
    return 1

