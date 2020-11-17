import argparse
import functools
import os
import pkgutil
import subprocess
import sys

from packaging.version import Version

from . import install_pip_package

try:
    from . import ctext
except ImportError:
    import ctext

print = ctext.print
input = ctext.input

__version__ = "1.0.1"


def requires_version(version: str):
    if Version(version) >= Version(__version__):
        raise EnvironmentError(
            f"autopyb>={version} is required, install by installing latest version of 'denver-api'"
        )


def run_command(command):
    if isinstance(command, str):
        return_code = os.system(command)
    else:
        return_code = subprocess.run(
            command, stderr=sys.stderr, stdout=sys.stdout, stdin=sys.stdin
        ).returncode
    return return_code


def get_module_list():
    return [x.name for x in pkgutil.iter_modules()]


def ensure_pip_package(package, t="STABLE"):
    if t.lower() == "stable":
        install_pip_package(package)
    elif t.lower() == "pre":
        install_pip_package(package, pre=True)
    elif t.lower() == "latest":
        install_pip_package(package, update=True)
    elif t.lower() == "pre-latest":
        install_pip_package(package, pre=True, update=True)
    else:
        print(
            f"type '{t}' is not a valid option, skipping installation for '{package}'",
            fore="yellow",
        )


def make_platform_executable(
    name: str, script: str, t="ONEFILE", extras=None, hidden=None, *aflags
):
    if "pyinstaller" not in get_module_list():
        install_pip_package("pyinstaller")
    if hidden is None:
        hidden = []
    if extras is None:
        extras = []
    t = [x.lower() for x in t.split("-")]
    print(f"Making platform executable '{name}'")
    flags: list = list(aflags)
    flags.extend(["-n", name])
    for x in extras:
        flags.extend(["--add-data", x])
    for x in hidden:
        flags.extend(["--hidden-import", x])
    if "onefile" in t:
        flags.append("--onefile")
    if "noconsole" in t:
        flags.append("-w")
    if run_command([sys.executable, "-m", "pyinstaller", script, *flags]) != 0:
        raise EnvironmentError("PyInstaller Failed")


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
                function(arguments)
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
                            f"{{fore_green}}----{{back_red}}{{fore_yellow}}end{{reset_all}}{{style_bright}}{{fore_green}}"
                            + f"------{x.__name__}-------------"
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
