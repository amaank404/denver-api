"""
Colored Text for beautiful output to the screen.
Anyone can use this in python application.
Also Colorama is present here by default. and
is used. This Module is tested with windows and
is perfect for cross-platform applications
which target *nix, Windows, etc.

You can try advanced color with ctext2 module which uses prompt toolkit
for 4-bit (8 colors), 8-bit (256 colors), 24-bit truecolor.

ctext2 is recommended
"""

__version__ = "2021.2.24"
__author__ = "Xcodz"

import builtins

if __name__ != "__main__":
    try:
        from . import _colorama as colorama
    except ImportError:
        import _colorama as colorama
else:
    import _colorama as colorama

import shutil
import sys

colorama.init()


def get_terminal_size():
    return shutil.get_terminal_size()


def clear_line(mode=2):
    print(colorama.ansi.clear_line(mode), end="", flush=True)


def clear_screen(mode=2):
    print(colorama.ansi.clear_screen(mode), end="", flush=True)


def style_text(text: str = " ", fore="none", style="none", back="none"):
    return escape(
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


def code_to_chars(code):
    return colorama.ansi.code_to_chars(code)


def set_title(title):
    print(colorama.ansi.set_title(title))


class Cursor:
    @staticmethod
    def print_at(x=1, y=1, text: str = " ", fore="none", style="none", back="none"):
        Cursor.set_position(x, y)
        print(style_text(text, fore=fore, back=back, style=style))

    @staticmethod
    def set_position(x=1, y=1):
        print(colorama.ansi.Cursor.POS(x, y))

    @staticmethod
    def up(n=1):
        print(colorama.ansi.Cursor.UP(n))

    @staticmethod
    def down(n=1):
        print(colorama.ansi.Cursor.DOWN(n))

    @staticmethod
    def left(n=1):
        print(colorama.ansi.Cursor.BACK(n))

    @staticmethod
    def right(n=1):
        print(colorama.ansi.Cursor.FORWARD(n))


def escape(text: str):
    return text.format(**escape_sequence)


colored_text_escape_sequence_back = {
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
colored_text_escape_sequence_fore = {
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
style_escape_sequence = {
    "bright": colorama.Style.BRIGHT,
    "dim": colorama.Style.DIM,
    "normal": colorama.Style.NORMAL,
    "none": "",
}
reset_escape_sequence = {
    "fore": colorama.Fore.RESET,
    "back": colorama.Back.RESET,
    "all": colorama.Style.RESET_ALL + colorama.Back.RESET + colorama.Fore.RESET,
    "none": "",
}
common_escape_sequence = {"none": ""}


def s(t, d):
    return {t + "_" + k: v for k, v in d.items()}


escape_sequence = {}
escape_sequence.update(
    **common_escape_sequence,
    **s("reset", reset_escape_sequence),
    **s("style", style_escape_sequence),
    **s("fore", colored_text_escape_sequence_fore),
    **s("back", colored_text_escape_sequence_back),
)

del s


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
            style_text(
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
    except Exception:
        builtins.print(*text, sep=sep, flush=flush, file=file, end=end)


def input(prompt="", fore="none", back="none", style="bright"):
    print(prompt, fore=fore, back=back, style=style, end="", flush=True)
    return builtins.input()
