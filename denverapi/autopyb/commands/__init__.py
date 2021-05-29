"""
The top level commands package. This package imports all the submodules and is imported by autopyb so
after import everything from autopyb all the subpackages will be available in global namespace.

See sub-modules for different available helper functions.
"""

from packaging.version import Version

from ... import autopyb
from . import distribution, pip, terminal


def requires_version(version: str):
    """
    It ensures that at least this version of autopyb is running. This was implemented at the starting itself to make sure
    that this works with every version of autopyb
    """
    if Version(version) > Version(autopyb.__version__):
        raise EnvironmentError(
            f"autopyb>={version} is required, install by installing latest version of 'denver-api'"
        )
