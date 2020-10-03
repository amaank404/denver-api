from denver import bcli
from denver import ctext
import os

cli = bcli.new_cli()


def tool(path):
    p = os.path.basename(path)
    p = os.path.splitext(p)[0]
    return p


if __name__ == '__main__':
    directory = os.path.dirname(__file__)
    # noinspection PyCallByClass
    print(ctext.ColoredText.escape("{green} Type"))
    cli.info("Available Tools")
    for x in os.listdir(directory):
        if not x.startswith("_"):
            cli.info("\t", tool(x), sep='')
