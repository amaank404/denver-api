"""
Provides utilities to log functions (Useful for debugging)

Example:

```python
from denverapi.function_logger import FunctionLogger

log_file = open("log_file.txt", "w")
logger = FunctionLogger(file=log_file)

@logger.debug
def run(greeting):
    print(greeting)

@logger.debug(action="Running Main")
def main():
    for x in range(3):
        run("Hello World")

main()
```

the above should save this to the file:

```
Running Main: main()
Running: run('Hello World')
Running: run('Hello World')
Running: run('Hello World')
```

this can be pretty neat and handy in place of print debugging.
"""

__version__ = "2020.10.31"
__author__ = "Xcodz"


import functools
import sys


class FunctionLogger:
    """
    Create a function logger object.

    `file` can be a stream that accepts text. if `echo` is enabled the function wrapped with debug logs
    to the file or else it just plainly runs the function.
    """

    def __init__(self, echo=True, file=sys.stdout):
        self.echo = echo
        self.file = file

    def debug(self, _func=None, action="Running"):
        """
        Wrap the given function in such a way that it logs to the `file` if `echo` is true.

        the action is used in the following format: `{action}: {function_representation}`
        """

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
                    self.file.flush()
                return func(*args, **kwargs)

            return function

        if _func is None:
            return decor
        else:
            return decor(_func)
