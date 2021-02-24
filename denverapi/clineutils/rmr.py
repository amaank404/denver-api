import argparse
import glob
from os import path, remove
from sys import exit

from denverapi.colored_text import print


def main():
    parser = argparse.ArgumentParser("rmr")
    parser.add_argument(
        "file", help="the file to remove (can be a glob pattern)", nargs="*", default=[]
    )
    args = parser.parse_args()
    if not isinstance(args.file, list):
        args.file = [args.file]
    for file in args.file:
        for x in glob.iglob(file, recursive=False):
            try:
                if path.isfile(x):
                    remove(x)
                else:
                    print(f"Directory: {x} is a directory", fore="red")
            except PermissionError:
                print(f"Permission Denied: {x}", fore="red")
                exit(1)


if __name__ == "__main__":
    main()
