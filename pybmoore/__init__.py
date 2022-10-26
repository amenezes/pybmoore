from ._boyer_moore import search

try:
    from . import _bm  # type: ignore
except ModuleNotFoundError:
    raise RuntimeError("Failed to load _bm module.")

__version__ = "1.3.0"
__all__ = ["search", "__version__"]
