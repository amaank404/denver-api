from packaging.version import Version

from ... import autopyb
from . import distribution, pip, terminal


def requires_version(version: str):
    if Version(version) > Version(autopyb.__version__):
        raise EnvironmentError(
            f"autopyb>={version} is required, install by installing latest version of 'denver-api'"
        )
