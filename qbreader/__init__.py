"""The official qbreader API python wrapper.

.. note::
    Even though useful type aliases defined in `qbreader.types` are reexported here,
    they are not documented here by `sphinx-autodoc`, but are documented in the
    `types` module.

    See:
        * https://github.com/sphinx-doc/sphinx/issues/8547
        * https://github.com/sphinx-doc/sphinx/issues/1063
"""

import importlib.metadata

import qbreader.types as types
from qbreader.asynchronous import Async
from qbreader.synchronous import Sync
from qbreader.types import *  # noqa: F401, F403
__version__ = importlib.metadata.version("qbreader")
__all__ = (
    "Async",
    "Sync",
    "types",
)

# add all symbols from qbreader.types to __all__
__all__ += types.__all__  # type: ignore

del importlib
