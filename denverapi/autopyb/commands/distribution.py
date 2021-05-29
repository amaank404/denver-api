"""
Provides distribution building specific functions
"""

import os
import shutil
import sys

from .pip import ensure_pip_package
from .terminal import run_command


def make_platform_executable(
    name: str, script: str, *aflags, t="ONEFILE", extras=None, hidden=None
):
    """
    This function can be used to make a native platform executable out of plain python scripts using
    pyinstaller>=3.0.0

    `name` is the executable title (name). while the `script` points to a single python script.
    If you want to package a module you will have to wrap the package using a wrapper script.

    `t` is the type of executable. By default it is ONEFILE which can be just changed to ''

    `extras` is a list of extra data files

    `hidden` is a list of modules imported by your script that are not detected by pyinstaller.
    This can be useful if modules are imported using importlib or something similar.

    `aflags` are the the flags provided such as `--windowed`.

    A full argument example:

    ```python
    distribution.make_platform_executable(
        "Hello World",
        "hello_world",
        "--windowed", # flags
        "--add-data", # flags
        "datafile.txt" # flags
        t="",
        extras=["settings.json"],
        hidden=['secrets'],
        )
    ```
    """
    ensure_pip_package("pyinstaller", ">=3")
    if hidden is None:
        hidden = []
    if extras is None:
        extras = []
    t = [x.lower() for x in t.split("-")]
    if os.path.isdir("dist"):
        shutil.rmtree("dist")

    print(f"Making platform executable '{name}'")
    flags: list = list(aflags)
    flags.extend(["-n", name])
    for x in extras:
        flags.extend(["--add-data", x])
    for x in hidden:
        flags.extend(["--hidden-import", x])
    if t.lower() == "ONEFILE":
        flags.append("--onefile")
    if "noconsole" in t:
        flags.append("-w")
    if run_command([sys.executable, "-m", "pyinstaller", script, *flags]) != 0:
        raise EnvironmentError("PyInstaller Failed")
