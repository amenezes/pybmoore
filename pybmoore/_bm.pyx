import cython

from ._bm cimport calc_offset, term_index


cdef int calc_offset(badchar_d: cython.int, goodsuffix_d: cython.int):
    if badchar_d > goodsuffix_d:
        return badchar_d
    return goodsuffix_d


cdef int term_index(offset: cython.int, suffix_len: cython.int):
    return (offset - suffix_len) - 1


cdef bint flag(int term_index, str suffix_char, str pattern_char):
    if (term_index > 0) or (suffix_char != pattern_char):
        return 0
    return 1


cpdef search(pattern: str, source: str):
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
            i += calc_offset(badchar_shift, goodsuffix_shift)
        else:
            r.append((i, i + pattern_len))
            i += 1
    return r


cdef bad_char_shift(str pattern):
    pattern_len: cython.int = len(pattern) - 1
    return {pattern[i]: (pattern_len - i) for i in range(pattern_len)}


cdef suffix_shift(str pattern):
    pattern_len: cython.int = len(pattern)
    skip_list = {}
    _buffer = ""
    for badchar in reversed(pattern):
        skip_list[len(_buffer)] = suffix_position(
            badchar, _buffer, pattern, pattern_len
        )

        _buffer = f"{_buffer}{badchar}"
    return skip_list


cdef int suffix_position(str badchar, str suffix, str pattern, int pattern_len):
    suffix_len: cython.int = len(suffix)
    for offset in reversed(range(1, pattern_len + 1)):
        flag_active: cython.bint = 1
        tindex = term_index(offset, suffix_len)
        for suffix_index in range(suffix_len):
            flag_active: cython.bint = flag(
                tindex,
                suffix[suffix_index],
                pattern[tindex + suffix_index]
            )
        if flag_active and (tindex <= 0 or pattern[tindex - 1] != badchar):
            return pattern_len - offset + 1

