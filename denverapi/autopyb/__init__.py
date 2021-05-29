"""
AutoPyB allows you to create clean looking build scripts in python (I hate MAKEFILES).
To get started we will create a simple example which showcases its power.

here is what is looks like:

```python
from denverapi.autopyb import *
import sys

requires_version("1.1.1")

tasks = BuildTasks()

@tasks.task()
def my_dependency_task():
    '''
    My Dependency Help Description
    '''
    # For more info on below modules check denverapi.autopyb.commands

    pip.ensure_pip_package("some_package")  # Any Version
    pip.ensure_pip_package("pygame", ">=2.0.0")  # With Version Specifier
    pip.ensure_pip_package_latest("pip")  # Install the latest (stable) package
    pip.ensure_pip_package_latest("pymunk", "pre")  # Install the latest (unstable) package 
                                                    # (by default the second argument is 'stable')
    
    terminal.run_command([sys.executable, "-m", "pip", "install", "flask"])
    terminal.run_command("apt install python")

    distribution.make_platform_executable("Hello World", "hello_world.py")  # It is way more customizable (check the docs)

    print("Doing Dependency Work")


@tasks.task(my_dependency_task)
def my_run_build():
    '''
    Builds using dependency
    '''
    print("All Done!")


if __name__ == '__main__':
    tasks.interact()

```
"""

import argparse
import functools
import sys
import textwrap

from .commands import *

try:
    from .. import colored_text
except ImportError:
    import denverapi.colored_text

print = colored_text.print
input = colored_text.input

__version__ = "1.1.0"


# noinspection PyCallByClass
class BuildTasks:
    """
    This class registers functions as tasks and creates a good looking cli out of it.
    See the module documentation for more information.
    """

    def __init__(self):
        self.ignored_tasks = []
        self.accomplished = []
        self.tasks = []

    def task(self, *dependencies, forced=False, ignored=False, uses_commandline=False):
        """
        A decorator for registering tasks.
        dependencies can contain a mix of Callable or Tuple[function: Callable, arguments: List[str]].

        if forced == True: task runs even if it has been executed already earlier as a dependency <br/>
        else: task runs if it has never been run before

        The above behaviour can be useful if you create a task that cleans up stuff and is required to run every time
        without skipping.

        if ignored == True: Do not show it as a available visible task to cli <br/>
        else: Show it as a normal available task to cli

        The above behaviour can be used to hide behind the scenes build task.

        if uses_commandline: Pass a list of arguments to the function as a single variable
        else: Call the function without any variables

        This can be useful for tasks that require command line arguments. Also
        if you have a dependency that uses this behaviour you need to pass the dependency as a tuple/list
        of function and a list of arguments: Tuple[function: Callable, arguments: List[str]]
        """

        def decorator(function):
            @functools.wraps(function)
            def wrapper_function(arguments=None):
                if arguments is None:
                    arguments = []
                print(
                    colored_text.escape(
                        f"{{fore_green}}----{{back_green}}{{fore_white}}start{{reset_all}}{{style_bright}}{{fore_green}}"
                        + f"----{function.__name__}-------------"
                    )
                )
                for depend in dependencies:
                    is_list = False
                    if callable(depend):
                        x = depend
                    elif isinstance(depend, (tuple, list)):
                        x = depend[0]
                        is_list = True
                    else:
                        raise TypeError(
                            "dependencies must be a function or a tuple[function: callable, [...]]"
                        )
                    if x not in self.accomplished:
                        print(
                            f"Running Task {x.__name__} (from {function.__name__})",
                            fore="magenta",
                        )
                        if x not in self.ignored_tasks:
                            self.accomplished.append(x)
                        try:
                            if is_list:
                                x(depend[1])
                            else:
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
                    colored_text.escape(
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
        """
        this function starts and parses the provided arguments using cli.

        if arguments is provided: arguments is used or else the sys.argv[1:] is used
        """
        if arguments is None:
            arguments = sys.argv[1:]
        parser = argparse.ArgumentParser()
        task_list = []
        command = parser.add_subparsers(dest="command_")
        for x in self.tasks:
            task_list.append(x.__name__)
            doc_help = (
                x.__doc__ if x.__doc__ is not None else "Help Not Provided"
            ).strip("\n")
            command.add_parser(x.__name__, help=textwrap.dedent(doc_help))
        args = parser.parse_args(arguments[0:1])
        for x in self.tasks:
            if args.command_ == x.__name__:
                try:
                    x(arguments[1:])
                except KeyboardInterrupt:
                    print("User aborted the process", fore="red")
                    print(
                        colored_text.escape(
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
                        colored_text.escape(
                            f"{{fore_green}}----{{back_red}}{{fore_yellow}}end{{reset_all}}{{style_bright}}{{"
                            "fore_green}" + f"------{x.__name__}-------------"
                        )
                    )
