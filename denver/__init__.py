"""
Denver is a project targeting python developers for easy and fast development
with the modules provided within it.
"""

__author__ = 'Xcodz'
__version__ = '2020.10.23'

import sys
import subprocess
from . import (bcli,
               bdtp,
               bdtpfserv,
               bitmap,
               crypt,
               ctext,
               datau,
               datp,
               dlic,
               get,
               graphics3d,
               graphics2d,
               handypy,
               log,
               pysetup,
               rawd,
               sound,
               text,
               cpic)


def install_pip_package(package: str, pre=False, update=False) -> int:
    arguments = [sys.executable, "-m", "pip", "install", package]
    if pre:
        arguments.append("--pre")
    if update:
        arguments.append("--update")
    return subprocess.run([sys.executable, "-m", "pip", "install", package], stdout=sys.stdout, stdin=sys.stdin,
                          stderr=sys.stderr).returncode
