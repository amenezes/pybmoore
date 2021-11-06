from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import singledispatch
from typing import Dict, List, Tuple

from pybmoore import _bm  # type: ignore


@singledispatch
def search(pattern: List[str], source: str) -> Dict:
    resp = {}
    pattern_len = len(pattern)
    with ProcessPoolExecutor(max_workers=pattern_len) as executor:
        futures = {
            executor.submit(_search, pattern[i], source) for i in range(pattern_len)
        }
        for future in as_completed(futures):
            term, result = future.result()
            resp[term] = result
    return resp


def _search(pattern: str, source: str):
    return pattern, search(pattern, source)


@search.register(str)  # type: ignore
def _(pattern: str, source: str) -> List[Tuple[int, int]]:
    return _bm.search(pattern, source)  # type: ignore
