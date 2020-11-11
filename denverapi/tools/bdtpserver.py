from denverapi import bdtpfserv
from denverapi import bcli
import argparse
import os

__version__ = "1.0.0"
__author__ = "Xcodz"

if __name__ == "__main__":
    cli = bcli.new_cli()

    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest="command", required=True)
    host = commands.add_parser("host", description="Host your very own file server")
    get = commands.add_parser("get", description="Get a file from server")
    post = commands.add_parser("post", description="Post a file to server")
    new = commands.add_parser("new_directory", description="Create a directory")
    dir_lister = commands.add_parser("list", description="List a directory")

    get.add_argument("-f", "--file", help="Path to file to get", required=True)
    get.add_argument(
        "-i", "--ip-address", help="IP Address of server", default="127.0.0.1"
    )
    get.add_argument("-p", "--port", help="Port to the server", required=True, type=int)
    get.add_argument(
        "-s",
        "--store",
        help="File to store, defaults to file's base name",
        default=None,
    )

    post.add_argument("-f", "--file", help="File to post", required=True)
    post.add_argument(
        "-i", "--ip-address", help="IP Address of server", default="127.0.0.1"
    )
    post.add_argument(
        "-p", "--port", help="Port to the server", required=True, type=int
    )
    post.add_argument(
        "-s",
        "--store",
        help="Path for the file to be stored on server, defaults to file's basename",
        default=None,
    )

    new.add_argument("-d", "--directory", help="Directory Name", required=True)
    new.add_argument(
        "-i", "--ip-address", help="IP Address of server", default="127.0.0.1"
    )
    new.add_argument("-p", "--port", help="Port to the server", required=True, type=int)

    dir_lister.add_argument(
        "-i", "--ip-address", help="IP Address of server", default="127.0.0.1"
    )
    dir_lister.add_argument(
        "-p", "--port", help="Port to the server", required=True, type=int
    )
    dir_lister.add_argument(
        "-d", "--directory", help="Directory to list", required=True
    )

    host.add_argument(
        "-i", "--ip-address", help="IP Address of server", default="127.0.0.1"
    )
    host.add_argument(
        "-p", "--port", help="Port to the server", required=True, type=int
    )
    host.add_argument(
        "-e",
        "--post-directory",
        help="Allow the post of users to be limited to this directory",
        default=None,
    )
    host.add_argument("-d", "--directory", help="Host Directory", default=".")

    parser.add_argument("-v", "--version", action="version")
    parser.add_argument("--no-log", action="store_true", help="Do not log to stdout")

    parser.version = "Copyright (c) 2020 Xcodz. bdtpserver {}".format(__version__)

    args = parser.parse_args()

    try:
        if args.command == "host":
            if not args.no_log:
                cli.info("Hosting Process Started")
                cli.info("IP Address :", args.ip_address)
                cli.info("Port       :", args.port)
            bdtpfserv.host(
                args.directory, (args.ip_address, args.port), args.post_directory
            )
        elif args.command == "get":
            if not args.no_log:
                cli.info("Getting file", args.file)
            data = bdtpfserv.get(args.file, (args.ip_address, args.port))
            if not args.no_log:
                cli.good(f"Download Complete ({len(data) // 1024} Kb)")
                cli.info("Writing File")
            file_to_write = args.store
            if file_to_write is None:
                file_to_write = os.path.basename(args.file)
            with open(file_to_write, "w+b") as file:
                file.write(data)
            if not args.no_log:
                cli.good("File Written")
        elif args.command == "post":
            if not args.no_log:
                cli.info("Reading file")
            with open(args.file, "r+b") as file:
                data = file.read()
            if not args.no_log:
                cli.good(f"File Read ({len(data) // 1024} Kb)")
                cli.info("Posting to server")
            file_to_write = args.store
            if file_to_write is None:
                file_to_write = os.path.basename(args.file)
            bdtpfserv.post(file_to_write, data, (args.ip_address, args.port))
            if not args.no_log:
                cli.good("Done Posting")
        elif args.command == "new_directory":
            if not args.no_log:
                cli.info("Making Directory")
            bdtpfserv.mkdir(args.directory, (args.ip_address, args.port))
            if not args.no_log:
                cli.good("Directory Made")
        elif args.command == "list":
            directory_list = bdtpfserv.listdir(
                args.directory, (args.ip_address, args.port)
            )
            cli.info('Directory listing of "', args.directory, '":', sep="")
            for x in directory_list:
                cli.info("\t", x)
    except KeyboardInterrupt:
        if not args.no_log:
            cli.bad("Process aborted by user")
        raise SystemExit(1)
    except Exception as exception:
        if not args.no_log:
            cli.bad("Exception", str(exception))
    if not args.no_log:
        cli.good("Process Complete")
