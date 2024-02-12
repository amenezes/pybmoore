from ._boyer_moore import search, search_m

try:
    from . import _bm  # type: ignore
except ModuleNotFoundError:
    raise RuntimeError("Failed to load _bm module.")

__version__ = "2.0.0"
__all__ = ["search", "search_m", "__version__"]
