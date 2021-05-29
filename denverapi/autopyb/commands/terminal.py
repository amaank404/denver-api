import os

"""
Provides terminal related function
"""

import subprocess
import sys
from typing import List, Union


def run_command(command: Union[List[str], str]):
    """
    A simple wrapper over `os.system` and `subprocess.run`

    If a List[str] is provided then the command is executed using `subprocess.run`, and if it is a string
    the command is executed with `os.system`.

    Examples available in `denverapi.autopyb`
    """
    if isinstance(command, str):
        return_code = os.system(command)
    else:
        return_code = subprocess.run(
            command, stderr=sys.stderr, stdout=sys.stdout, stdin=sys.stdin
        ).returncode
    return return_code
