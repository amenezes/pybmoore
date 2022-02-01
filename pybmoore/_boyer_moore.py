from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import singledispatch
from typing import Any, Dict, List, Tuple

from pybmoore import _bm  # type: ignore


@singledispatch
def search(pattern: Any, source: str) -> Dict:
    """Search for some pattern in the source

    :param pattern: pattern value to search. (Valid values: str, List[str] or Tuple[str])
    :param source: source data.
    """
    raise NotImplementedError(
        f"Pattern must be str, List[str] or Tuple[str] got {type(pattern)}"
    )


@search.register(list)
@search.register(tuple)
def _(pattern: List[str], source: str) -> Dict:
    resp = {}
    pattern_len = len(pattern)
    with ProcessPoolExecutor(max_workers=pattern_len) as executor:
        futures = {
            executor.submit(_search_job, pattern[i], source) for i in range(pattern_len)
        }
        for future in as_completed(futures):
            term, result = future.result()
            resp[term] = result
    return resp


def _search_job(pattern: str, source: str):
    return pattern, search(pattern, source)


@search.register(str)
def _(pattern: str, source: str) -> List[Tuple[int, int]]:
    return _bm.search(pattern, source)  # type: ignore
