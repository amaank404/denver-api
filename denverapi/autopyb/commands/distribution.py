from .terminal import run_command
from .pip import get_module_list
import sys
from ... import install_pip_package


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
