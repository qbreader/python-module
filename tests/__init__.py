from typing import Callable
from urllib.request import urlopen

import pytest


def check_internet_connection():
    """Check if there is an internet connection."""
    try:
        urlopen("https://www.qbreader.org")
        return True
    except Exception:
        return


# do not run tests if there is no internet connection
assert check_internet_connection(), "No internet connection"


def assert_exception(
    func: Callable,
    exception,
    *args,
    **kwargs,
):
    """Assert that a function raises an exception."""
    with pytest.raises(exception):
        func(*args, **kwargs)


def assert_warning(
    func: Callable,
    warning,
    *args,
    **kwargs,
):
    """Assert that a function raises a warning."""
    with pytest.warns(warning):
        return func(*args, **kwargs)
