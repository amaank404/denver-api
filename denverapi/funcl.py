"""
Function Logs
"""

__version__ = "2020.10.31"
__author__ = "Xcodz"


import functools
import sys


class FunctionLogger:
    def __init__(self, echo=True, file=sys.stdout):
        self.echo = True
        self.file = file

    def debug(self, _func=None, *, action="Running"):
        def decor(func):
            @functools.wraps(func)
            def function(*args, **kwargs):
                if self.echo:
                    nargs = [repr(x) for x in args]
                    nkwargs = {k: repr(v) for k, v in kwargs.items()}
                    statement = func.__name__ + "("
                    if len(nargs) != 0:
                        statement += ", ".join(nargs)
                    if len(nargs) != 0 and len(nkwargs) != 0:
                        statement += ", "
                    if len(nkwargs) != 0:
                        statement += ", ".join([f"{k}={v}" for k, v in nkwargs.items()])
                    statement += ")"
                    print(f"{action}: {statement}", file=self.file)
                func(*args, **kwargs)

            return function

        if _func is None:
            return decor
        else:
            return decor(_func)
