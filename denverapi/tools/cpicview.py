import argparse

from denverapi import cpic


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="file to view")
    args = parser.parse_args()
    print(cpic.combine(cpic.read_image(args.file)))
