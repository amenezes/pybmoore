from functools import singledispatch
from typing import Dict, List, Tuple

from pybmoore import _bm  # type: ignore


@singledispatch
def search(pattern: List[str], source: str) -> Dict:
    return {criteria: _bm.search(criteria, source) for criteria in pattern}


@search.register(str)  # type: ignore
def _(pattern: str, source: str) -> List[Tuple[int, int]]:
    return _bm.search(pattern, source)  # type: ignore
