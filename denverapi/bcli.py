"""
================================
Beautiful Command Line Interface
================================
........
2020.6.5
........

What does it do?
================

It helps in making of beautiful
CLI with different level print
functions. Also it supports
"""

__version__ = "2020.6.5"
__author__ = "Xcodz"

import sys

try:
    from . import ctext
except ImportError:
    import ctext


class Beauty_CLI:
    """
    Beauty Command Line Interface
    =============================

    This interface is used to make the
    output text seem beautiful. there
    are 5 main beauty functions. run,
    good, bad and info are for output.
    input is for taking input from the
    stdin.
    """

    def __init__(self, file, fmt_function):
        self.file = file
        self.fmt = fmt_function

    def _print_mode(self, *obj, file=None, end="\n", sep=" ", flush=False, mode="n"):
        """
        emulates the default print function but with a different mode
        """
        if file is None:
            file = self.file
        ostr = []
        for x in obj:
            if isinstance(x, str):
                ostr.append(x)
            else:
                ostr.append(repr(x))
        if mode == "n":
            print(*ostr, sep=sep, flush=flush, file=file, end=end)
        else:
            print(
                self.fmt(sep.join(ostr), mode), sep=sep, flush=flush, file=file, end=end
            )

    def good(self, *obj, file=None, end="\n", sep=" ", flush=False):
        """
        emulates the default print function for good mode
        """
        self._print_mode(*obj, file=file, end=end, sep=sep, flush=flush, mode="g")

    def bad(self, *obj, file=None, end="\n", sep=" ", flush=False):
        """
        emulates the default print function for bad mode
        """
        self._print_mode(*obj, file=file, end=end, sep=sep, flush=flush, mode="b")

    def info(self, *obj, file=None, end="\n", sep=" ", flush=False):
        """
        emulates the default print function for info mode
        """
        self._print_mode(*obj, file=file, end=end, sep=sep, flush=flush, mode="i")

    def input(self, prompt=None):
        """
        emulates the default input function for query mode
        """
        if prompt is None:
            prompt = ""
        self._print_mode(prompt, end="", flush=True, mode="q")
        return input()

    def run(self, *obj, file=None, end="\n", sep=" ", flush=False):
        """
        emulates the default print function for run mode
        """
        self._print_mode(*obj, file=file, end=end, sep=sep, flush=flush, mode="r")


def _fmt_bcli(text, m):
    if m == "i":
        return "\033[93m[!] " + text + ctext.ColoredText.resetEscapeSequence["all"]
    if m == "q":
        return "\033[94m[?] " + text + ctext.ColoredText.resetEscapeSequence["all"]
    if m == "b":
        return "\033[91m[-] " + text + ctext.ColoredText.resetEscapeSequence["all"]
    if m == "g":
        return "\033[92m[+] " + text + ctext.ColoredText.resetEscapeSequence["all"]
    if m == "r":
        return "\033[97m[~] " + text + ctext.ColoredText.resetEscapeSequence["all"]


def new_cli(file=sys.stdout, fmt="bcli") -> Beauty_CLI:
    return Beauty_CLI(file, eval(f"_fmt_{fmt}"))


def main():
    mcli = new_cli()
    mcli.info("This is 'info'")
    mcli.good("This is 'good'")
    mcli.bad("This is 'bad'")
    mcli.run("This is 'run'")
    mcli.input("This is 'input'")


if __name__ == "__main__":
    main()
