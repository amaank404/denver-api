import argparse
import glob
import shutil
from os import path
from sys import exit

from denverapi.ctext import print


def main():
    parser = argparse.ArgumentParser("rmrdir")
    parser.add_argument(
        "directory", help="the directory to recursively remove (can be a glob pattern)"
    )
    args = parser.parse_args()
    for x in glob.iglob(args.directory, recursive=False):
        try:
            if path.isdir(x):
                shutil.rmtree(x)
            else:
                print(f"File: {x} is a file", fore="red")
        except PermissionError:
            print(f"Permission Denied: {x}", fore="red")
            exit(1)
