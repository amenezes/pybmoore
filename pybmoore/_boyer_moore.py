from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import singledispatch
from typing import List, Set, Tuple, Union

from pybmoore import _bm  # type: ignore


@singledispatch
def search(
    pattern: Union[str, List[str], Set[str], Tuple[str]], source: str, *args, **kwargs
) -> List[Tuple[int, int]]:
    """Search for some pattern in the source.

    Usage:

    # str pattern
    pybmoore.search(
        'printing',
        'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
    )

    # List[str] pattern
    pybmoore.search(
        ['printing', 'text'],
        'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
    )

    # Set[str] pattern
    pybmoore.search(
        {'printing', 'text'},
        'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
    )

    # Tuple[str] pattern
    pybmoore.search(
        ('printing', 'text'),
        'Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
    )

    > *args and **kwargs parameters are used only for search with List[str] or Tuple[str] patterns.

    :param pattern: pattern value to search. (Valid values: str, List[str] or Tuple[str]).
    :param source: source data.
    :param *args: args for ProcessPoolExecutor.
    :param **kwargs: kwargs for ProcessPoolExecutor.
    """
    raise NotImplementedError(
        f"Pattern '{type(pattern)}' not supported. See available options in the pybmoore.search help."
    )


@search.register(str)
def _(pattern, source, *args, **kwargs):
    if len(pattern) == 0:
        return []
    return _bm.search(pattern, source)


@search.register(list)
def _(pattern, source, *args, **kwargs):
    return search(tuple(pattern), source)


@search.register(set)
def _(pattern, source, *args, **kwargs):
    return search(tuple(pattern), source)


@search.register(tuple)
def _(pattern, source, *args, **kwargs):
    resp = {}
    with ProcessPoolExecutor(*args, **kwargs) as executor:
        futures = {
            executor.submit(_search_job, pattern[i], source)
            for i in range(len(pattern))
        }
        for future in as_completed(futures):
            term, result = future.result()
            resp[term] = result
    return resp


def _search_job(pattern: str, source: str) -> Tuple[str, List[Tuple[int, int]]]:
    return pattern, search(pattern, source)
