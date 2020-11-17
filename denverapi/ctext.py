"""
Colored Text for beautiful output to the screen.
Anyone can use this in python application.
Also Colorama is present here by default. and
is used. This Module is tested with windows and
is perfect for cross-platform applications
which target *nix, Windows, etc.
"""

__version__ = "2020.6.4"
__author__ = "Xcodz"

import builtins

if __name__ != "__main__":
    try:
        from . import _colorama as colorama
    except:
        import _colorama as colorama
else:
    import _colorama as colorama

import os
import shutil
import sys

colorama.initialise.init()


# noinspection PyCallByClass
class ColoredText:
    def getTerminalSize():
        return shutil.get_terminal_size()

    def clearLine(mode=2):
        print(colorama.ansi.clear_line(mode), end="", flush=True)

    def clearScreen(mode=2):
        print(colorama.ansi.clear_screen(mode), end="", flush=True)

    def styleText(text: str = " ", fore="none", style="none", back="none"):
        return ColoredText.escape(
            "{fore_"
            + fore
            + "}{back_"
            + back
            + "}{style_"
            + style
            + "}"
            + text
            + "{reset_all}"
        )

    def codeToChars(code):
        return colorama.ansi.code_to_chars(code)

    def setTitle(title):
        print(colorama.ansi.set_title(title))

    class Cursor:
        def printat(x=1, y=1, text: str = " ", fore="none", style="none", back="none"):
            print(
                ColoredText.Cursor.pos(x, y)
                + ColoredText.styleText(text, fore=fore, back=back, style=style)
            )

        def pos(x=1, y=1):
            print(colorama.ansi.Cursor.POS(x, y))

        def up(n=1):
            print(colorama.ansi.Cursor.UP(n))

        def down(n=1):
            print(colorama.ansi.Cursor.DOWN(n))

        def left(n=1):
            print(colorama.ansi.Cursor.BACK(n))

        def right(n=1):
            print(colorama.ansi.Cursor.FORWARD(n))

    def escape(Text: str):
        return Text.format(**ColoredText.escapeSequence)

    cloredTextEscapeSequenceBack = {
        "black": colorama.Back.BLACK,
        "blue": colorama.Back.BLUE,
        "red": colorama.Back.RED,
        "green": colorama.Back.GREEN,
        "yellow": colorama.Back.YELLOW,
        "magenta": colorama.Back.MAGENTA,
        "cyan": colorama.Back.CYAN,
        "white": colorama.Back.WHITE,
        "lightblack": colorama.Back.LIGHTBLACK_EX,
        "lightred": colorama.Back.LIGHTRED_EX,
        "lightgreen": colorama.Back.LIGHTGREEN_EX,
        "lightyellow": colorama.Back.LIGHTYELLOW_EX,
        "lightblue": colorama.Back.LIGHTBLUE_EX,
        "lightmagenta": colorama.Back.LIGHTMAGENTA_EX,
        "lightcyan": colorama.Fore.LIGHTCYAN_EX,
        "lightwhite": colorama.Fore.LIGHTWHITE_EX,
        "none": "",
    }
    cloredTextEscapeSequenceFore = {
        "black": colorama.Fore.BLACK,
        "blue": colorama.Fore.BLUE,
        "red": colorama.Fore.RED,
        "green": colorama.Fore.GREEN,
        "yellow": colorama.Fore.YELLOW,
        "magenta": colorama.Fore.MAGENTA,
        "cyan": colorama.Fore.CYAN,
        "white": colorama.Fore.WHITE,
        "lightblack": colorama.Fore.LIGHTBLACK_EX,
        "lightred": colorama.Fore.LIGHTRED_EX,
        "lightgreen": colorama.Fore.LIGHTGREEN_EX,
        "lightyellow": colorama.Fore.LIGHTYELLOW_EX,
        "lightblue": colorama.Fore.LIGHTBLUE_EX,
        "lightmagenta": colorama.Fore.LIGHTMAGENTA_EX,
        "lightcyan": colorama.Fore.LIGHTCYAN_EX,
        "lightwhite": colorama.Fore.LIGHTWHITE_EX,
        "none": "",
    }
    styleEscapeSequence = {
        "bright": colorama.Style.BRIGHT,
        "dim": colorama.Style.DIM,
        "normal": colorama.Style.NORMAL,
        "none": "",
    }
    resetEscapeSequence = {
        "fore": colorama.Fore.RESET,
        "back": colorama.Back.RESET,
        "all": colorama.Style.RESET_ALL + colorama.Back.RESET + colorama.Fore.RESET,
        "none": "",
    }
    commonEscapeSequence = {"none": ""}


def s(t, d):
    return {t + "_" + k: v for k, v in d.items()}


d = {}
d.update(
    **ColoredText.commonEscapeSequence,
    **s("reset", ColoredText.resetEscapeSequence),
    **s("style", ColoredText.styleEscapeSequence),
    **s("fore", ColoredText.cloredTextEscapeSequenceFore),
    **s("back", ColoredText.cloredTextEscapeSequenceBack),
)

ColoredText.escapeSequence = d

del d, s


def print(
    *text,
    fore="none",
    back="none",
    style="bright",
    sep=" ",
    end="\n",
    flush=False,
    file=sys.stdout,
):
    try:
        builtins.print(
            ColoredText.styleText(
                sep.join([x if type(x) == str else repr(x) for x in text]),
                fore=fore,
                back=back,
                style=style,
            ),
            sep=sep,
            flush=flush,
            file=file,
            end=end,
        )
    except Exception as e:
        builtins.print(*text, sep=sep, flush=flush, file=file, end=end)


def input(prompt="", fore="none", back="none", style="bright"):
    print(prompt, fore=fore, back=back, style=style, end="", flush=True)
    return builtins.input()
