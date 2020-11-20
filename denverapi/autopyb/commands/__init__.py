from ... import autopyb
from packaging.version import Version

from . import terminal
from . import pip
from . import distribution


def requires_version(version: str):
    if Version(version) >= Version(autopyb.__version__):
        raise EnvironmentError(
            f"autopyb>={version} is required, install by installing latest version of 'denver-api'"
        )
