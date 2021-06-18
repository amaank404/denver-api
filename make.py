import glob
from sys import executable

from denverapi.autopyb import *

auto = BuildTasks()

# Information
requires_version("1.1.0")


@auto.task()
def clean():
    """
    Try Removing All Cache Files
    """
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
    """
    Install Package in Development mode using poetry.
    """
    pip.ensure_pip_package("poetry")
    terminal.run_command([executable, "-m", "poetry", "install"])


@auto.task(clean)
def build():
    """
    Make Two types of distribution
    """
    pip.ensure_pip_package("wheel")
    pip.ensure_pip_package("setuptools")
    terminal.run_command([executable, "setup.py", "sdist", "bdist_wheel"])


@auto.task(clean)
def style():
    """
    Format code for meeting our repository guidelines
    """
    print("Checking Pip requirements")
    pip.ensure_pip_package("black", ">=20.8.b1")
    pip.ensure_pip_package("isort", ">=5.6.4")

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


@auto.task()
def check():
    """
    Check if code matches our code contribution guidelines
    """
    pip.ensure_pip_package("black", ">=20.8b1")
    pip.ensure_pip_package("codespell", ">=2.0.0")
    pip.ensure_pip_package("flake8", ">=3.8.4")
    pip.ensure_pip_package("isort", ">=5.6.4")
    print("\nChecking code")
    print(" BLACK")
    if terminal.run_command([sys.executable, "-m", "black", "--check", "."]):
        raise Exception("black Failed")
    print("\n\n ISORT")
    if terminal.run_command([sys.executable, "-m", "isort", "--profile", "black", "."]):
        raise Exception("isort Failed")
    print("\n\n FLAKE8")
    if terminal.run_command(
        [
            sys.executable,
            "-m",
            "flake8",
            ".",
            "--count",
            "--select=E9,F63,F7,F82",
            "--show-source",
            "--statistics",
        ]
    ):
        raise Exception("flake8 Failed")
    print("\n\n CODESPELL")
    terminal.run_command([sys.executable, "-m", "codespell_lib", "-q", "2"])
    print("check codespell carefully (if it finds problem in '.git', then ignore this)")


if __name__ == "__main__":
    auto.interact()
