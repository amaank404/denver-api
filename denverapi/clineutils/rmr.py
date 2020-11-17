import argparse
import glob
from os import path, remove
from sys import exit

from denverapi.ctext import print


def main():
    parser = argparse.ArgumentParser("rmrdir")
    parser.add_argument("file", help="the file to remove (can be a glob pattern)")
    args = parser.parse_args()
    for x in glob.iglob(args.file, recursive=False):
        try:
            if path.isfile(x):
                remove(x)
            else:
                print(f"Directory: {x} is a directory", fore="red")
        except PermissionError:
            print(f"Permission Denied: {x}", fore="red")
            exit(1)
