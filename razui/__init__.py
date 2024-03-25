import sys

if sys.platform == "darwin":
    # apple bad
    raise OSError("Don't use RazUI on MacOS smh") from None

from .window import *
from .object import *