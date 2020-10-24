"""
PiOS Package Kit
================

The Official Build Tools for PiOS
"""

import json
import os
import shutil
import argparse
import pickle
import sys


class PPK:
    def __init__(self):
        self.config = None
        self.installer = None
        self.packages = []
        self.py_modules = []
        self.data_directories = []
        self.data_files = []
        self.main_package = None
        self.icon = None
        self.requirement = []
        self.sdk_packages = []

    def add_directory(self, directory):
        self.data_directories.append(directory)

    def set_configuration(self, configuration_file):
        with open(configuration_file) as file:
            self.config = json.load(file)

    def set_custom_installer(self, installer_file):
        with open(installer_file) as file:
            self.installer = file.read()

    def add_package(self, package):
        self.packages.append(package)

    def add_sdk_package(self, name):
        self.sdk_packages.append(name)

    def add_file(self, file):
        self.data_files.append(file)

    def add_module(self, module):
        self.py_modules.append(module)

    def add_pip_requirement(self, requirement, update=False, pre=False):
        self.requirement.append((requirement, pre, update))

    def set_main_package(self, package):
        self.main_package = package

    def set_icon(self, icon: str):
        self.icon = icon

    def build(self):
        if 'pios_build' in os.listdir():
            shutil.rmtree("pios_build")
        os.mkdir("pios_build")
        os.mkdir("pios_build/assets")
        os.mkdir("pios_build/lib")
        with open("pios_build/setup.py", "w") as file:
            file.write(self.installer)
        with open("pios_build/app.json", "w") as file:
            json.dump(self.config, file, indent=4, sort_keys=True)
        with open("pios_build/requirements.pickle", "w+b") as file:
            pickle.dump(self.requirement, file)
        for x in self.data_directories:
            shutil.copytree(x, f"pios_build/assets/{os.path.basename(x)}")
        for x in self.data_files:
            shutil.copyfile(x, f"pios_build/assets/{os.path.basename(x)}")
        shutil.copyfile(self.icon, "pios_build/icon.cpg")
        for x in self.packages:
            shutil.copytree(x, f"pios_build/packages/{os.path.basename(x)}")
        for x in self.sdk_packages:
            shutil.copytree(f"{__file__}/library/{x}", f"pios_build/packages/{os.path.basename(x)}")
        for x in self.py_modules:
            shutil.copyfile(x, f"pios_build/packages/{os.path.basename(x)}")
        shutil.copytree(self.main_package, "pios_build/main")

    @staticmethod
    def package():
        if "dist" not in os.listdir():
            os.mkdir("dist")
        shutil.make_archive("pios_build/ppk", "zip", "pios_build")
        shutil.copyfile("pios_build/ppk.zip", "dist/app-main.ppk")

    def load_using_json(self, file="build.json"):
        with open(file) as file:
            config = json.load(file)
        self.set_icon(config["icon"])
        self.set_main_package(config["main_package"])
        self.set_custom_installer(config["installer"])
        self.set_configuration(config["configuration"])
        for x in config["requirements"]:
            self.add_pip_requirement(x)
        for x in config["data_files"]:
            self.add_file(x)
        for x in config["data_directories"]:
            self.add_directory(x)
        for x in config["packages"]:
            self.add_package(x)
        for x in config["modules"]:
            self.add_module(x)
        for x in config["sdk_packages"]:
            self.add_sdk_package(x)


def main(arguments):
    parser = argparse.ArgumentParser(description="PPK Package Tool", fromfile_prefix_chars="@")
    options = parser.add_mutually_exclusive_group()
    setup_modifier = options.add_argument_group()
    setup_modifier.add_argument("-p", "--package", help="add a python package to build list", action="append", 
                                default=[])
    setup_modifier.add_argument("-P", "--sdk-package", help="add a local copy of sdk library to packages",
                                action="append", default=[])
    setup_modifier.add_argument("-m", "--module", help="add a python module to build list", action="append", default=[])
    setup_modifier.add_argument("-r", "--pypi-requirement", help="add a python pypi package to build list",
                                action="append", default=[])
    setup_modifier.add_argument("-ad", "--add-directory", help="add a directory to build list", action="append",
                                default=[])
    setup_modifier.add_argument("-af", "--add-file", help="add a file to to build list", action="append", default=[])
    setup_modifier.add_argument("-i", "--installer", help="add a custom installer to build list", default=None)
    setup_modifier.add_argument("-c", "--configure", help="add a app configuration to build list", default="app.json")
    setup_modifier.add_argument("-mp", "--main-package", help="set a main package", default="main")
    setup_modifier.add_argument("--icon", help="set a icon for your Application", default="icon.cpg")
    options.add_argument("-b", "--build", help="Build the ppk using 'build.json' file", action="store_true")
    options.add_argument("-ppk", "--pios-package-kit", help="Packages the final app into PPK", action="store_true")
    options.add_argument("--cleanup", help="Cleanup the directory be deleting unnecessary data", action="store_true")

    args = parser.parse_args(arguments)

    if args.build:
        app = PPK()
        app.load_using_json()
        app.build()
    elif args.cleanup:
        if "pios_build" in os.listdir():
            shutil.rmtree("pios_build")
    elif args.pios_package_kit:
        app = PPK()
        app.load_using_json()
        app.package()
    else:
        if args.installer is None:
            args.installer = os.path.abspath(f"{__file__}/../_installer.py")
        config = {"icon": args.icon,
                  "main_package": args.main_package,
                  "installer": args.installer,
                  "configuration": args.configure,
                  "requirements": args.pypi_requirement,
                  "data_files": args.add_file,
                  "data_directories": args.add_directory,
                  "packages": args.package,
                  "modules": args.module,
                  "sdk_packages": args.sdk_package}
        with open("build.json", "w") as file:
            json.dump(config, file, sort_keys=True, indent=4)


if __name__ == '__main__':
    main(sys.argv[1:])
