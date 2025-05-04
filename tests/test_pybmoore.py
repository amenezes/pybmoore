from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import pytest

import pybmoore


@pytest.mark.skip(reason="function tuned for use of Cython-specific cdef statement")
@pytest.mark.parametrize(
    "pattern, expected",
    [
        (
            "refactoring",
            {"a": 7, "c": 6, "e": 9, "f": 8, "i": 2, "n": 1, "o": 4, "r": 3, "t": 5},
        ),
        ("lei", {"l": 2, "e": 1}),
        ("test", {"t": 3, "e": 2, "s": 1}),
    ],
)
def test_bad_char_shift(pattern, expected):
    assert pybmoore._bm.bad_char_shift(pattern) == expected


@pytest.mark.skip(reason="function tuned for use of Cython-specific cdef statement")
@pytest.mark.parametrize(
    "pattern, expected",
    [
        ("amor", {0: 1, 1: 4, 2: 4, 3: 4}),
        ("lei", {0: 1, 1: 3, 2: 3}),
        (
            "refactoring",
            {
                0: 1,
                1: 11,
                2: 11,
                3: 11,
                4: 11,
                5: 11,
                6: 11,
                7: 11,
                8: 11,
                9: 11,
                10: 11,
            },
        ),
    ],
)
def test_suffix_shift(pattern, expected):
    assert pybmoore._bm.suffix_shift(pattern) == expected


@pytest.mark.skip(reason="function tuned for use of Cython-specific cdef statement")
@pytest.mark.parametrize(
    "badchar, suffix, pattern, expected",
    [
        ("r", "", "amor", 1),
        ("o", "r", "amor", 4),
        ("m", "or", "amor", 4),
        ("a", "mor", "amor", 4),
    ],
)
def test_suffix_position(badchar, suffix, pattern, expected):
    assert (
        pybmoore._bm.suffix_position(badchar, suffix, pattern, len(pattern)) == expected
    )


@pytest.mark.parametrize(
    "pattern, expected",
    [
        (
            "algorithm",
            [
                (51, 60),
                (94, 103),
                (374, 383),
                (538, 547),
                (809, 818),
                (969, 978),
                (997, 1006),
                (1076, 1085),
            ],
        ),
        ("string-searching", [(77, 93)]),
        (["19", [(238, 240), (522, 524)]]),
        ("constant factor", [(923, 938)]),
        ("The Boyer–Moore", [(793, 808)]),
        ("string-search", [(37, 50), (77, 90), (149, 162)]),
        ("computer science,", [(3, 20)]),
        ("algorithm preprocess", [(538, 558)]),
        ("Wojciech Rytter", [(503, 518)]),
        ("", []),
    ],
)
def test_search(pattern, expected):
    TEXT = """In computer science, the Boyer–Moore string-search algorithm is an efficient string-searching algorithm that is the standard benchmark for practical string-search literature.[1] It was developed by Robert S. Boyer and J Strother Moore in 1977.[2] The original paper contained static tables for computing the pattern shifts without an explanation of how to produce them. The algorithm for producing the tables was published in a follow-on paper; this paper contained errors which were later corrected by Wojciech Rytter in 1980.[3][4] The algorithm preprocesses the string being searched for (the pattern), but not the string being searched in (the text). It is thus well-suited for applications in which the pattern is much shorter than the text or where it persists across multiple searches. The Boyer–Moore algorithm uses information gathered during the preprocess step to skip sections of the text, resulting in a lower constant factor than many other string search algorithms. In general, the algorithm runs faster as the pattern length increases. The key features of the algorithm are to match on the tail of the pattern rather than the head, and to skip along the text in jumps of multiple characters rather than searching every single character in the text."""
    assert pybmoore.search(pattern, TEXT) == expected


@pytest.mark.parametrize(
    "pattern, expected",
    [
        ("Section", 56),
        ("freedom", 1),
        ("Congress", 60),
        ("Congress of the United States", 1),
    ],
)
def test_search_with_large_text_us(us_constitution_text, pattern, expected):
    assert len(pybmoore.search(pattern, us_constitution_text)) == expected


@pytest.mark.parametrize(
    "pattern, expected",
    [
        ("Deus", 3),
        ("Lei nº", 49),
        ("Brasil", 41),
        ("§ 1º", 293),
        ("Supremo Tribunal Federal", 62),
    ],
)
def test_search_with_large_text_br(br_constitution_text, pattern, expected):
    assert len(pybmoore.search(pattern, br_constitution_text)) == expected


@pytest.mark.parametrize(
    "patterns, expected, executor",
    [
        (
            ["freedom", "Congress"],
            {"freedom": 1, "Congress": 60},
            ThreadPoolExecutor,
        ),
        (
            ["freedom", "Congress"],
            {"freedom": 1, "Congress": 60},
            ProcessPoolExecutor,
        ),
        (
            {"freedom", "Congress"},
            {"freedom": 1, "Congress": 60},
            ThreadPoolExecutor,
        ),
        (
            {"freedom", "Congress"},
            {"freedom": 1, "Congress": 60},
            ProcessPoolExecutor,
        ),
        (
            ("freedom", "Congress"),
            {"freedom": 1, "Congress": 60},
            ThreadPoolExecutor,
        ),
        (
            ("freedom", "Congress"),
            {"freedom": 1, "Congress": 60},
            ProcessPoolExecutor,
        ),
        (
            "Congress",
            {"Congress": 60},
            ThreadPoolExecutor,
        ),
        (
            "freedom",
            {"freedom": 1},
            ProcessPoolExecutor,
        ),
    ],
)
def test_search_multiple_terms_us(us_constitution_text, patterns, expected, executor):
    result = pybmoore.search_m(patterns, us_constitution_text, executor)
    assert result.keys() == expected.keys()
    for pattern, expected_count in expected.items():
        assert len(result[pattern]) == expected_count


@pytest.mark.parametrize(
    "patterns, expected, executor",
    [
        (["Deus", "Brasil"], {"Deus": 3, "Brasil": 41}, ThreadPoolExecutor),
        (["Lei nº", "§ 1º"], {"Lei nº": 49, "§ 1º": 293}, ProcessPoolExecutor),
        ({"Deus", "Brasil"}, {"Deus": 3, "Brasil": 41}, ThreadPoolExecutor),
        ({"Lei nº", "§ 1º"}, {"Lei nº": 49, "§ 1º": 293}, ProcessPoolExecutor),
        (("Deus", "Brasil"), {"Deus": 3, "Brasil": 41}, ThreadPoolExecutor),
        (("Lei nº", "§ 1º"), {"Lei nº": 49, "§ 1º": 293}, ProcessPoolExecutor),
        ("Deus", {"Deus": 3}, ThreadPoolExecutor),
        ("Lei nº", {"Lei nº": 49}, ProcessPoolExecutor),
    ],
)
def test_search_multiple_terms_br(br_constitution_text, patterns, expected, executor):
    result = pybmoore.search_m(patterns, br_constitution_text, executor)
    assert result.keys() == expected.keys()
    for pattern, expected_count in expected.items():
        assert len(result[pattern]) == expected_count


@pytest.mark.parametrize("pattern", [-1.0, -1, 1.0, 1, None, True, False, {}])
def test_not_implemented_search(pattern):
    with pytest.raises(NotImplementedError):
        pybmoore.search(pattern, "Python/Cython Boyer-Moore string-search algorithm")


@pytest.mark.parametrize("pattern", [-1.0, -1, 1.0, 1, None, True, False, {}])
def test_not_implemented_search_m(pattern):
    with pytest.raises(NotImplementedError):
        pybmoore.search_m(
            pattern,
            "Python/Cython Boyer-Moore string-search algorithm",
            ThreadPoolExecutor,
        )
