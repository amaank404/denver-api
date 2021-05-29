"""
Prints a list of all available tools
"""

import os

from denverapi import beautiful_cli

cli = beautiful_cli.new_cli()


def tool(path):
    p = os.path.basename(path)
    p = os.path.splitext(p)[0]
    return p


if __name__ == "__main__":
    directory = os.path.dirname(__file__)
    cli.info("Available Tools")
    for x in os.listdir(directory):
        if not x.startswith("_") and x.endswith(".py"):
            cli.info("\t", tool(x), sep="")
