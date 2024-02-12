from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


import pytest

import pybmoore


@pytest.mark.parametrize(
    "filename, terms, executor",
    [
        (
            "tests/data/br_constitution.txt",
            ["Deus", "Brasil"],
            ThreadPoolExecutor
        ),
        (
            "tests/data/br_constitution.txt",
            ["Supremo Tribunal Federal", "Emenda Constitucional"],
            ThreadPoolExecutor
        ),
    ],
)
def test_search_multiple_terms_thread_pool(filename, terms, executor, benchmark):
    benchmark(pybmoore.search_m, terms, Path(filename).read_text(), executor)


@pytest.mark.parametrize(
    "filename, terms, executor",
    [
        (
            "tests/data/br_constitution.txt",
            ["Deus", "Brasil"],
            ProcessPoolExecutor
        ),
        (
            "tests/data/br_constitution.txt",
            ["Supremo Tribunal Federal", "Emenda Constitucional"],
            ProcessPoolExecutor
        ),
    ],
)
def test_search_multiple_terms_process_pool(filename, terms, executor, benchmark):
    benchmark(pybmoore.search_m, terms, Path(filename).read_text(), executor)


@pytest.mark.parametrize(
    "filename,term",
    [
        ("tests/data/br_constitution.txt", "Lei nº"),
        ("tests/data/br_constitution.txt", "Supremo Tribunal Federal"),
        ("tests/data/us_constitution.txt", "Congress"),
        ("tests/data/us_constitution.txt", "Congress of the United States"),
    ],
)
def test_search_single_term(filename, term, benchmark):
    benchmark(pybmoore.search, term, Path(filename).read_text())



@pytest.mark.parametrize(
    "pattern",
    [
        ("algorithm"),
        ("string-searching"),
        ("19"),
        ("The Boyer–Moore"),
        ("algorithm preprocess"),
    ],
)
def test_search(pattern, benchmark):
    TEXT = "In computer science, the Boyer–Moore string-search algorithm is an efficient string-searching algorithm that is the standard benchmark for practical string-search literature.[1] It was developed by Robert S. Boyer and J Strother Moore in 1977.[2] The original paper contained static tables for computing the pattern shifts without an explanation of how to produce them. The algorithm for producing the tables was published in a follow-on paper; this paper contained errors which were later corrected by Wojciech Rytter in 1980.[3][4] The algorithm preprocesses the string being searched for (the pattern), but not the string being searched in (the text). It is thus well-suited for applications in which the pattern is much shorter than the text or where it persists across multiple searches. The Boyer–Moore algorithm uses information gathered during the preprocess step to skip sections of the text, resulting in a lower constant factor than many other string search algorithms. In general, the algorithm runs faster as the pattern length increases. The key features of the algorithm are to match on the tail of the pattern rather than the head, and to skip along the text in jumps of multiple characters rather than searching every single character in the text."
    benchmark(pybmoore.search, pattern, TEXT)

