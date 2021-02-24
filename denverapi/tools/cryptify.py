import argparse

from denverapi import encryption


def main():
    parser = argparse.ArgumentParser(description="Encrypt and Decrypt files")
    parser.add_argument(
        "-m",
        "--mode",
        help="Mode of encryption, (d: decrypt, e: encrypt)",
        choices=["d", "e"],
        default="e",
    )
    parser.add_argument("password")
    parser.add_argument("input_file")
    parser.add_argument("output_file", nargs="?", default=None)
    args = parser.parse_args()

    with open(args.input_file, "rb") as file:
        data = file.read()

    data = (encryption.encrypt if args.mode == "e" else encryption.decrypt)(
        data, args.password
    )

    if args.output_file is None:
        args.output_file = args.input_file

    with open(args.output_file, "wb") as file:
        file.write(data)


if __name__ == "__main__":
    main()
