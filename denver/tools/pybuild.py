"""
pybuild allows users to generate and package projects using a single python written configuration file
"""

import os
import shutil
import argparse
from denver import dlic
import configparser


def parse_info(info):
    if not info["package"]:
        info["package"] = info["name"]
    if not info["version"]:
        info["version"] = '1.0.0'
    if not info["requirements"]:
        info["requirements"] = []
    else:
        info["requirements"] = info["requirements"].split(",")


def c_new(arg):
    if arg.from_file:
        config_info = configparser.ConfigParser()
        config_info.read(arg.from_file)
        info = config_info["pybuild"]
    else:
        info = {}
        print("Project Information:")
        info["name"] = input("Project Name >")
        info["package"] = input(f"Main Package [{info['name']}]>")
        info["version"] = input("Version [1.0.0]>")
        info["description"] = input("Short Description>")
        info["requirements"] = input("Requirements (Comma Seperated) [None]>")
    parse_info(info)
    config_script = f"""
# Project Metadata
NAME = {repr(info['name'])}
VERSION = {repr(info["version"])}
SHORT_DESCRIPTION = {repr(info["description"])}
PACKAGE = {repr(info["package"])}
REQUIREMENTS = [{', '.join(["'"+x+"'" for x in info["requirements"]])}]


# Build Types
# It can be a list of the options
#
# You can specify setup.py options like this
#     setup your_build_type
# In the above statement your_build_type can be anything you want
# For example:
#     setup sdist
#     setup bdist_wheel
# 
# You can also specify a few inbuilt options like this
#     build your_build_type
# In the above statement your_build_type can be one of the following
#     pios_app
#     pyinstaller_exe
# A few of the above may require extra configuration for which you can use the variable mentioned next
BUILD_TYPES = ["setup sdist",
               "setup bdist_wheel"]


# pios app
# pios requires a app.json and a build.json file inside the root directory of project

# pyinstaller_exe
# to configure pyinstaller you will need to create a pyinstaller.txt file under root directory of project

# setup can be configured by the following variables
# you can specify you variable by following syntax
#     SETUP_{{Setup Argument}} = {{Value}}
SETUP_name = NAME
SETUP_version = VERSION
SETUP_description = SHORT_DESCRIPTION
SETUP_long_description = open("README.md").read()
SETUP_long_description_content_type = "text/markdown"

"""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Manage small project with this tool")
    commands = parser.add_subparsers(dest="command", required=True)

    new = commands.add_parser("new", description="Create a new project")
    new.add_argument("--from-file", help="Use options from file without launching the command line interface",
                     default=False)

    args = parser.parse_args()

    if args.command == "new":
        c_new(args)
