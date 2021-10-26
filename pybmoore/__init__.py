from .__version__ import __version__
from ._boyer_moore import search

try:
    from . import _bm  # type: ignore
except ModuleNotFoundError:
    raise RuntimeError("Failed to load _bm module.")


__all__ = ["search"]
