from pathlib import Path

import pytest

import pybmoore


@pytest.mark.skip
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


@pytest.mark.skip
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


@pytest.mark.skip
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
    "pattern,expected",
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
    ],
)
def test_search(pattern, expected):
    TEXT = "In computer science, the Boyer–Moore string-search algorithm is an efficient string-searching algorithm that is the standard benchmark for practical string-search literature.[1] It was developed by Robert S. Boyer and J Strother Moore in 1977.[2] The original paper contained static tables for computing the pattern shifts without an explanation of how to produce them. The algorithm for producing the tables was published in a follow-on paper; this paper contained errors which were later corrected by Wojciech Rytter in 1980.[3][4] The algorithm preprocesses the string being searched for (the pattern), but not the string being searched in (the text). It is thus well-suited for applications in which the pattern is much shorter than the text or where it persists across multiple searches. The Boyer–Moore algorithm uses information gathered during the preprocess step to skip sections of the text, resulting in a lower constant factor than many other string search algorithms. In general, the algorithm runs faster as the pattern length increases. The key features of the algorithm are to match on the tail of the pattern rather than the head, and to skip along the text in jumps of multiple characters rather than searching every single character in the text."
    assert pybmoore.search(pattern, TEXT) == expected


@pytest.mark.parametrize(
    "filename,term,expected",
    [
        ("tests/data/br_constitution.txt", "Deus", 3),
        ("tests/data/br_constitution.txt", "Lei nº", 49),
        ("tests/data/br_constitution.txt", "Brasil", 41),
        ("tests/data/br_constitution.txt", "§ 1º", 293),
        ("tests/data/br_constitution.txt", "Supremo Tribunal Federal", 62),
        ("tests/data/us_constitution.txt", "Section", 56),
        ("tests/data/us_constitution.txt", "freedom", 1),
        ("tests/data/us_constitution.txt", "Congress", 60),
        ("tests/data/us_constitution.txt", "Congress of the United States", 1),
    ],
)
def test_search_with_large_text(filename, term, expected):
    assert len(pybmoore.search(term, Path(filename).read_text())) == expected


@pytest.mark.parametrize(
    "filename,terms,expected",
    [
        (
            "tests/data/br_constitution.txt",
            ["Deus", "Brasil"],
            {"Deus": 3, "Brasil": 41},
        ),
        (
            "tests/data/us_constitution.txt",
            ["freedom", "Congress"],
            {"freedom": 1, "Congress": 60},
        ),
    ],
)
def test_search_multiple_terms(filename, terms, expected):
    result = pybmoore.search(terms, Path(filename).read_text())
    assert result.keys() == expected.keys()
    assert sum([len(x) for x in result.values()]) == sum([x for x in expected.values()])
