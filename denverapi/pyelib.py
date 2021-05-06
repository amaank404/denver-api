"""
Utilities to generate a cached library out of python source
"""

import os
import types

import dill


def empty_module(name="__pye__", doc=""):
    return types.ModuleType(name, doc)


def make_pye(name: str, code: str):
    """
    Generate a PYE from source code
    """

    file = "lib" + os.path.basename(name) + ".pye"
    file_dir = os.path.dirname(name)

    module = empty_module()
    exec(code, module.__dict__)
    dill.dump_session(os.path.join(file_dir, file), module)
    return module


def load_pye(name: str, environment=None):
    """
    Load a PYE from file into dctionary of globals environment
    """
    module = empty_module()
    if environment is not None:
        module.__dict__ = environment

    file = "lib" + os.path.basename(name) + ".pye"
    file_dir = os.path.dirname(name)

    dill.load_session(os.path.join(file_dir, file), module)
    return module
