from contextlib import contextmanager
import sys

from fastcli.exceptions import FASTError
from fastcli.log import console


@contextmanager
def fast_error_handler():
    """Context manager to handle FASTError exceptions in a standard way."""
    try:
        yield
    except FASTError as e:
        console.error(str(e))
        sys.exit(1)
