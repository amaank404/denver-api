import json
import sys
import argparse


def make_empty_app(**configuration):
    with open("app.json", "w") as file:
        json.dump(configuration, file, indent=4, sort_keys=True)


def main(arguments):
    parser = argparse.ArgumentParser(description="Generate PiOS Project", fromfile_prefix_chars="@")
    parser.add_argument("-n", "--new", help="Generate empty project", action="store_true")
    parser.add_argument("--configure", help="", action="append", type=tuple)

    args = parser.parse_args(arguments)

    if args.new:
        make_empty_app()


if __name__ == '__main__':
    main(sys.argv[1:])
