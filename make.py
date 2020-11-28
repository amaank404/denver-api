import glob
from sys import executable

from denverapi.autopyb import *

auto = BuildTasks()

# Information
requires_version("1.1.0")


@auto.task()
def clean():
    print("Removing all __pycache__ directories")
    terminal.run_command(
        [
            executable,
            "-m",
            "denverapi.clineutils.rmrdir",
            "__pycache__",
            "**/__pycache__",
        ]
    )


@auto.task(clean)
def develop():
    terminal.run_command([executable, "setup.py", "develop"])


@auto.task(clean)
def style():
    print("Checking Pip requirements")
    modules = pip.get_module_list()
    if "black" not in modules:
        pip.ensure_pip_package("black")
    if "isort" not in modules:
        pip.ensure_pip_package("isort")
    print("\nCode Formatting using black")
    terminal.run_command([executable, "-m", "black", "."])
    print("\nCode Formatting using isort")
    terminal.run_command([executable, "-m", "isort", "."])

    print("\nConverting tabs to 4 spaces")
    print("  Gathering List")
    py_files = []
    for x in glob.iglob("**/*.py", recursive=False):
        py_files.append(x)
    for x in glob.iglob("*.py", recursive=False):
        py_files.append(x)
    print("  Formatting files")
    for x in py_files:
        with open(x) as file:
            data = file.read()
        data = data.replace("\t", " " * 4)
        with open(x, "w") as file:
            file.write(data)
    print("  Done")
    clean()


if __name__ == "__main__":
    auto.interact()
