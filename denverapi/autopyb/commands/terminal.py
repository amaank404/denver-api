import os
import subprocess
import sys


def run_command(command):
    if isinstance(command, str):
        return_code = os.system(command)
    else:
        return_code = subprocess.run(
            command, stderr=sys.stderr, stdout=sys.stdout, stdin=sys.stdin
        ).returncode
    return return_code
