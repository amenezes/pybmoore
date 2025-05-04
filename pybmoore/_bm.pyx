import cython
cimport cython

from ._bm cimport calc_offset, term_index


cdef int calc_offset(badchar_d: cython.int, goodsuffix_d: cython.int):
    if badchar_d > goodsuffix_d:
        return badchar_d
    return goodsuffix_d


cdef int term_index(offset: cython.int, suffix_len: cython.int):
    return (offset - suffix_len) - 1


cdef bint flag(int term_index, int suffix_char, int pattern_char):
    if (term_index > 0) or (suffix_char != pattern_char):
        return 0
    return 1


cpdef search(pattern: str, source: str):
    pattern_len: cython.int = len(pattern)
    source_len: cython.int = len(source)
    good_suffix = suffix_shift(pattern, pattern_len)
    bad_char = bad_char_shift(pattern, pattern_len - 1)
    r = []
    i: cython.int = 0
    badchar_shift: cython.int = 0

    while i < ((source_len - pattern_len) + 1):
        sliding_window: cython.int = pattern_len
        while (
            sliding_window > 0
            and pattern[sliding_window - 1] == source[i + sliding_window - 1]
        ):
            sliding_window -= 1
        if sliding_window > 0:
            try:
                badchar_shift = bad_char[source[i + sliding_window - 1]]
            except KeyError:
                badchar_shift = pattern_len
            goodsuffix_shift: cython.int = good_suffix[pattern_len - sliding_window]
            i += calc_offset(badchar_shift, goodsuffix_shift)
        else:
            r.append((i, i + pattern_len))
            i += 1
    return r


cdef dict bad_char_shift(str pattern, int pattern_len):
    shift_dict: dict = {}
    i: cython.int = 0
    for i in range(pattern_len):
        shift_dict[pattern[i]] = pattern_len - i
    return shift_dict


cdef dict suffix_shift(str pattern, int pattern_len):
    skip_dict: dict = {}
    _buffer = ""

    for badchar in reversed(pattern):
        skip_dict[len(_buffer)] = suffix_position(
            badchar, _buffer, pattern, pattern_len
        )
        _buffer = f"{_buffer}{badchar}"
    return skip_dict


cdef int suffix_position(str badchar, str suffix, str pattern, int pattern_len):
    ZERO: cython.int = 0
    ONE: cython.int = 1

    suffix_len: cython.int = len(suffix)
    suffix_index: cython.int = 0
    offset: cython.int = 1
    pattern_char_value: cython.int = 0
    suffix_char_value: cython.int = 0
    
    for offset in reversed(range(ONE, pattern_len + ONE)):
        flag_active: cython.bint = 1
        tindex: cython.int = term_index(offset, suffix_len)
        for suffix_index in range(suffix_len):
            pattern_char_value: cython.int = ord(pattern[tindex + suffix_index])
            suffix_char_value: cython.int = ord(suffix[suffix_index])
            flag_active: cython.bint = flag(
                tindex,
                suffix_char_value,
                pattern_char_value                
            )
        if flag_active and (tindex <= ZERO or pattern[tindex - ONE] != badchar):
            return pattern_len - offset + 1
