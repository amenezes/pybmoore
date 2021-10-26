from functools import singledispatch
from typing import Dict, List, Tuple

try:
    from . import _bm  # type: ignore
except ModuleNotFoundError:
    raise RuntimeError("Failed to load _bm module.")


@singledispatch
def search(pattern: List[str], source: str) -> Dict:
    return {criteria: _bm.search(criteria, source) for criteria in pattern}


@search.register(str)  # type: ignore
def _(pattern: str, source: str) -> List[Tuple[int, int]]:
    return _bm.search(pattern, source)  # type: ignore
