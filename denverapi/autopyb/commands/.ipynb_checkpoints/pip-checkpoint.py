import pkgutil

from ... import install_pip_package
from ...ctext import print


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
