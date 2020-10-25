import json
import sys
import argparse
import shutil
from typing import Tuple


class ConfigurationError(Exception):
    pass


def configuration_tuple(obj: str) -> Tuple[str]:
    return tuple(obj.split("=", 1))


required_configuration = [
    "name",
    "version",
]


def make_empty_app(**configuration):
    with open("app.json", "w") as file:
        json.dump(configuration, file, indent=4, sort_keys=True)
    for x in required_configuration:
        if x not in configuration.keys():
            raise ConfigurationError(f"The following configuration value is needed: {x}")
    shutil.copytree(f"{__file__}/../resources/template_package", "main")
    shutil.copyfile(f"{__file__}/../resources/icon.cpg", "icon.cpg")


def main(arguments):
    parser = argparse.ArgumentParser(description="Generate PiOS Project", fromfile_prefix_chars="@")
    parser.add_argument("-n", "--new", help="Generate empty project", action="store_true")
    parser.add_argument("-c", "--configure", help="Configure a project with key value pair", action="append",
                        type=configuration_tuple, default=[])
    args = parser.parse_args(arguments)

    if args.new:
        make_empty_app(**{key: value for (key, value) in args.configure})


if __name__ == '__main__':
    main(sys.argv[1:])
