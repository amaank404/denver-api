"""
Recursive version for importlib.reload

source from: https://gist.github.com/shwang/09bd0ffef8ef65af817cf977ce4698b8
"""

from importlib import reload
from types import ModuleType


def recursive_reload(module):
    """Recursively reload a module and all its submodules.
    Graph DFS strategy modified from
    https://stackoverflow.com/questions/15506971/recursive-version-of-reload
    """
    visited = set()

    def visit(m):
        if m in visited:
            return
        visited.add(m)
        for attribute_name in dir(m):
            attribute = getattr(m, attribute_name)
            if type(attribute) is ModuleType:
                visit(attribute)
        reload(m)

    visit(module)
