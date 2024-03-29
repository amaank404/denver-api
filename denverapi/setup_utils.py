"""
Utilities for setup

Like find package data for including all package data
into the setup.
"""

__version__ = "2020.6.8"
__author__ = "Xcodz"

import os


def find_package_data(package: str, package_name=None):
    """
    Find data inside a package. can be used for `setuptools.setup`

    Example:
    ```python
    from setuptools import setup
    from denverapi import setup_utils

    setup(
        ...
        package_data=setup_utils.find_package_data("my_package"),
        ...
    )
    ```
    """
    if package_name is None:
        package_name = package
    files = []
    for r, d, f in os.walk(package):
        files.extend([os.path.join(r, x)[len(package) + 1 :] for x in f])
    _exclude_files(files, [".py"])
    root = {}
    for x in files:
        d = x.split(os.sep)
        d.pop(-1)
        d = ".".join(d)
        root.setdefault(package_name + "." + d, [])
        root[package_name + "." + d].append(os.path.basename(x))
    return {k.strip("."): v for k, v in root.items()}


def _exclude_files(filespath: list, exts: list):
    rml = []
    for x in range(len(filespath)):
        if os.path.splitext(filespath[x])[1] in exts:
            rml.append(filespath[x])
    for x in rml:
        filespath.remove(x)


def concatenate_dictionaries(d1: dict, d2: dict, *d):
    """
    Concatenate two or multiple dictionaries. Can be used with multiple `find_package_data` return values.
    """
    base = d1
    base.update(d2)
    for x in d:
        base.update(x)
    return base


if __name__ == "__main__":
    from pprint import pprint

    os.chdir("..")
    pprint(find_package_data("denverapi", "denverapi"))
