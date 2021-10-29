cdef int calc_offset(int badchar_d, int goodsuffix_d)

cdef int term_index(int offset, int suffix_len)

cdef bint flag(int term_index, str suffix_char, str pattern_char)
