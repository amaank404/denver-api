import pkgutil

import pkg_resources
from packaging.requirements import Requirement
from packaging.version import Version

from ... import install_pip_package
from ...colored_text import print


def get_module_list():
    return [x.name for x in pkgutil.iter_modules()]


distribution_dict = {d.project_name: d.version for d in pkg_resources.working_set}
distribution_list = list(distribution_dict.keys())


def ensure_pip_package(package: str, v: str = ">=0"):
    version_requirement = f"{package}{v}"
    version_exists = distribution_dict.get(package, None)
    if version_exists is None:
        install_pip_package(f"{package}{v}")
    elif not evaluate_requirement(version_requirement, version_exists):
        install_pip_package(f"{package}{v}")
    return


def ensure_pip_package_latest(package: str, t: str = "stable"):
    if t.lower() == "stable":
        install_pip_package(package, update=True)
    elif t.lower() == "pre":
        install_pip_package(package, pre=True, update=True)
    else:
        print(
            f"type '{t}' is not a valid option, skipping installation for '{package}'",
            fore="yellow",
        )


def evaluate_requirement(requirement: str, version: str):
    req = Requirement(requirement)
    ver = Version(version)
    if len(req.extras) != 0:
        return False
    if req.marker is not None:
        if not req.marker.evaluate():
            return False
    return ver in req.specifier
