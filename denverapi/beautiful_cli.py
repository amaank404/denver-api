"""
# Beautiful Command Line Interface
## What does it do?

It helps in making of beautiful
CLI with different level print
functions. it also supports input function
"""

__version__ = "2021.2.24"
__author__ = "Xcodz"

import re
import shutil
import sys
import textwrap as ptw

import ansiwrap as tw

try:
    from . import colored_text
except ImportError:
    from denverapi import colored_text


es = colored_text.escape_sequence


class Beauty_CLI:
    """
    ### Beauty Command Line Interface

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

    def raw(self, *obj, file=None, end="\n", sep=" ", flush=False):
        """
        emulates the default print function without any formatting modifications
        """
        print(*obj, sep=sep, end=end, file=file, flush=flush)


def _fmt_bcli(text, m):
    if m == "i":
        return (
            f"{es['fore_yellow']}[!] "
            + text
            + colored_text.reset_escape_sequence["all"]
        )
    if m == "q":
        return (
            f"{es['fore_blue']}[?] "
            + text
            + colored_text.reset_escape_sequence["all"]
            + "\n>"
        )
    if m == "b":
        return (
            f"{es['fore_red']}[-] " + text + colored_text.reset_escape_sequence["all"]
        )
    if m == "g":
        return (
            f"{es['fore_green']}[+] " + text + colored_text.reset_escape_sequence["all"]
        )
    if m == "r":
        return (
            f"{es['reset_all']}[~] " + text + colored_text.reset_escape_sequence["all"]
        )


_http_re_pattern = re.compile(
    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)


def _arch_replace(text, m):

    p_start = es["fore_yellow"]

    if m == "r":
        p_end = es["reset_all"] + es["style_bright"]
    elif m == "i":
        p_end = es["reset_all"]
    elif m == "b":
        p_end = es["reset_all"]
    elif m == "g":
        p_end = es["reset_all"] + es["style_bright"] + es["fore_green"]
    else:
        p_end = es["reset_all"] + es["fore_magenta"]

    urls = set(re.findall(_http_re_pattern, text))
    for x in urls:
        text = text.replace(x, f"{p_start}{x}{p_end}")

    if m == "r":
        text = tw.fill(text, shutil.get_terminal_size().columns - 3)
        text = ptw.indent(text, " " * 3)[3:]

    return text


def _fmt_arch(text, m):
    text = _arch_replace(text, m)
    if m == "r":
        return f'\n{es["fore_green"]}::{es["reset_fore"]}{es["style_bright"]} {text}{es["reset_all"]}'
    if m == "i":
        return f'{es["fore_yellow"]}==> {es["style_bright"]}WARNING: {es["reset_all"]}{text}'
    if m == "b":
        return f'{es["fore_red"]}==> {es["style_bright"]}ERROR: {es["reset_all"]}{text}'
    if m == "g":
        return f'.. {es["fore_green"]+es["style_bright"]} {text} {es["reset_all"]}'
    if m == "q":
        return f':. {es["fore_magenta"]}{text}{es["reset_all"]}\n{es["fore_red"]}~{es["reset_all"]}'


def new_cli(file=sys.stdout, fmt="bcli") -> Beauty_CLI:
    """
    Creates a new CLI using format `fmt` and returns it.

    Available Formats:
    * arch
    * bcli (default)
    """
    return Beauty_CLI(file, eval(f"_fmt_{fmt}"))


def main():
    """
    This is a simple test that showcases different formats and BeautifulCLIs
    """
    for x in [
        x.split("_fmt_", 1)[1] for x in globals().keys() if x.startswith("_fmt_")
    ]:
        mcli = new_cli(fmt=x)
        mcli.info("This is 'info' this is url https://www.google.com/ and some text")
        mcli.good("This is 'good' this is url https://www.google.com/ and some text")
        mcli.bad("This is 'bad' this is url https://www.google.com/ and some text")
        mcli.run("This is 'run' this is url https://www.google.com/ and some text")
        mcli.input("This is 'input' this is url https://www.google.com/ and some text")


if __name__ == "__main__":
    main()
