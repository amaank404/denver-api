import argparse
import glob
import shutil
from os import path
from sys import exit

from denverapi.ctext import print


def main():
    parser = argparse.ArgumentParser("rmrdir")
    parser.add_argument(
        "directory",
        help="the directory to recursively remove (can be a glob pattern)",
        nargs="*",
        default=[],
    )
    args = parser.parse_args()
    if not isinstance(args.directory, list):
        args.directory = [args.directory]
    for directory in args.directory:
        for x in glob.iglob(directory, recursive=False):
            try:
                if path.isdir(x):
                    shutil.rmtree(x)
                else:
                    print(f"File: {x} is a file", fore="red")
            except PermissionError:
                print(f"Permission Denied: {x}", fore="red")
                exit(1)


if __name__ == "__main__":
    main()
