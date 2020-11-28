import argparse
import functools
import sys

from .commands import *

try:
    from .. import ctext
except ImportError:
    import denverapi.ctext

print = ctext.print
input = ctext.input

__version__ = "1.1.0"


# noinspection PyCallByClass
class BuildTasks:
    def __init__(self):
        self.ignored_tasks = []
        self.accomplished = []
        self.tasks = []

    def task(self, *dependencies, forced=False, ignored=False, uses_commandline=False):
        def decorator(function):
            @functools.wraps(function)
            def wrapper_function(arguments=None):
                if arguments is None:
                    arguments = []
                print(f"-------------{function.__name__}-------------", fore="green")
                for x in dependencies:
                    if x not in self.accomplished:
                        print(
                            f"Running Task {x.__name__} (from {function.__name__})",
                            fore="magenta",
                        )
                        if x not in self.ignored_tasks:
                            self.accomplished.append(x)
                        try:
                            x(None)
                        except Exception as e:
                            print(
                                f"Encountered {e.__class__.__name__}: {str(e)} ({x.__name__})",
                                fore="red",
                            )
                            sys.exit(1)
                    else:
                        print(
                            f"Skipped Task {x.__name__} (from {function.__name__})",
                            fore="cyan",
                        )
                if uses_commandline:
                    function(arguments)
                else:
                    function()
                print(
                    ctext.ColoredText.escape(
                        f"{{fore_green}}----{{back_red}}{{fore_yellow}}end{{reset_all}}{{style_bright}}{{fore_green}}"
                        + f"------{function.__name__}-------------"
                    )
                )

            if forced:
                self.ignored_tasks.append(wrapper_function)

            if not ignored:
                self.tasks.append(wrapper_function)

            return wrapper_function

        return decorator

    def interact(self, arguments=None):
        if arguments is None:
            arguments = sys.argv[1:]
        parser = argparse.ArgumentParser()
        command = parser.add_subparsers(dest="command_")
        for x in self.tasks:
            command.add_parser(x.__name__, description=x.__doc__)
        args = parser.parse_args(arguments[0:1])
        for x in self.tasks:
            if args.command_ == x.__name__:
                try:
                    x(arguments[1:])
                except KeyboardInterrupt:
                    print("User aborted the process", fore="red")
                    print(
                        ctext.ColoredText.escape(
                            f"{{fore_green}}----{{back_red}}{{fore_yellow}}end{{reset_all}}{{style_bright}}"
                            f"{{fore_green}} "
                            f"------{x.__name__}-------------"
                        )
                    )
                except Exception as e:
                    print(
                        f"Process Failed with {e.__class__.__name__}: {str(e)}",
                        fore="red",
                    )
                    print(
                        ctext.ColoredText.escape(
                            f"{{fore_green}}----{{back_red}}{{fore_yellow}}end{{reset_all}}{{style_bright}}{{fore_green}}"
                            + f"------{x.__name__}-------------"
                        )
                    )
