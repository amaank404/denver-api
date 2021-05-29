"""
Denver is a project targeting python developers for easy and fast development
with the modules provided within it. You can know what a module does by checking
its documentation.

*If in case you need help, please do not go over to stackoverflow or some other site
because most of the people you will find there will not be experienced with this library.
You can use GitHub issues page of this repository for that purpose.*
"""

__author__ = "Xcodz"
__version__ = "3.1.0"

import subprocess
import sys


def install_pip_package(package: str, pre=False, update=False) -> int:
    arguments = [sys.executable, "-m", "pip", "install", package]
    if pre:
        arguments.append("--pre")
    if update:
        arguments.append("--update")
    return subprocess.run(
        [sys.executable, "-m", "pip", "install", package],
        stdout=sys.stdout,
        stdin=sys.stdin,
        stderr=sys.stderr,
    ).returncode
