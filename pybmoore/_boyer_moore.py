from functools import singledispatch
from typing import Dict, List, Optional, Tuple


@singledispatch
def search(pattern: List[str], source: str) -> Dict:
    return {criteria: search(criteria, source) for criteria in pattern}


@search.register(str)  # type: ignore
def _(pattern: str, source: str) -> List[Tuple[int, int]]:
    good_suffix = suffix_shift(pattern)
    bad_char = bad_char_shift(pattern)
    pattern_size = len(pattern)
    source_size = len(source)
    r = []
    i = 0
    while i < ((source_size - pattern_size) + 1):
        j = pattern_size
        while j > 0 and pattern[j - 1] == source[i + j - 1]:
            j -= 1
        if j > 0:
            # badchar_shift = bad_char.get(source[i + j - 1], pattern_size)
            try:
                badchar_shift = bad_char[source[i + j - 1]]
            except KeyError:
                badchar_shift = pattern_size
            goodsuffix_shift = good_suffix[pattern_size - j]
            if badchar_shift > goodsuffix_shift:
                i += badchar_shift
            else:
                i += goodsuffix_shift
        else:
            r.append((i, i + pattern_size))
            i += 1
    return r


def bad_char_shift(pattern: str) -> Dict[str, int]:
    pattern_len = len(pattern) - 1
    return {pattern[i]: (pattern_len - i) for i in range(0, pattern_len)}


def suffix_shift(pattern: str) -> Dict:
    pattern_len = len(pattern)
    skip_list = {}
    _buffer = ""
    for i in range(0, pattern_len):
        badchar = pattern_len - 1 - i
        skip_list[len(_buffer)] = suffix_position(pattern[badchar], _buffer, pattern)
        _buffer = f"{pattern[badchar]}{_buffer}"
    return skip_list


def suffix_position(badchar: str, suffix: str, full_term: str) -> Optional[int]:
    full_term_size = len(full_term)
    suffix_size = len(suffix)
    resp = None
    for offset in range(1, full_term_size + 1)[::-1]:
        flag = True
        term_index = (offset - suffix_size) - 1
        for suffix_index in range(0, suffix_size):
            if (term_index > 0) or (
                suffix[suffix_index] != full_term[term_index + suffix_index]
            ):
                flag = False
        if flag and (term_index <= 0 or full_term[term_index - 1] != badchar):
            resp = full_term_size - offset + 1
            break
    return resp
