import argparse
import hashlib
import sys
import os


def main(arguments):
    parser = argparse.ArgumentParser(description="A tool to generate sha256 checksums for ppa, py, text, etc files")

    options = parser.add_mutually_exclusive_group()
    options.add_argument("-u", "--unicode", dest="mode", action="store_const", const="u")
    options.add_argument("-b", "--bytes", dest="mode", action="store_const", const="b")

    parser.add_argument("file", metavar="FILE", help="File is required to check for sha256", nargs="+", default=[])

    parser.set_defaults(mode="b")
    args = parser.parse_args(arguments)

    for x in args.file:
        if args.mode == "b":
            with open(x, "r+b") as file:
                data = file.read()
            with open(os.path.splitext(x)[0]+".b256", "w+b") as file:
                file.write(hashlib.sha256(data).digest())
        if args.mode == "u":
            with open(x) as file:
                data = file.read()
                data = data.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
            with open(os.path.splitext(x)[0]+".u256", "w+b") as file:
                file.write(hashlib.sha256(data).digest())


if __name__ == '__main__':
    main(sys.argv[1:])
