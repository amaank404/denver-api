"""
Colored Text for beautiful output to the screen.
Anyone can use this in python application.
Also Colorama is present here by default. and
is used. This Module is tested with windows and
is perfect for cross-platform applications
which target *nix, Windows, etc.
"""

__version__ = "2021.2.24"
__author__ = "Xcodz"

import builtins
import shutil
import sys

import colorama

colorama.init()


def get_terminal_size():
    """
    Wrapper over `shutil.get_terminal_size` for your convenience
    """
    return shutil.get_terminal_size()


def clear_line(mode=2):
    """
    Clear current line
    """
    print(colorama.ansi.clear_line(mode), end="", flush=True)


def clear_screen(mode=2):
    """
    Clear screen (using ANSI Escape Sequence)
    """
    print(colorama.ansi.clear_screen(mode), end="", flush=True)


def style_text(text: str = " ", fore="none", style="none", back="none"):
    """
    Style the provided text
    """
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
    """
    Wrapper over `colorama.ansi.code_to_chars`
    """
    return colorama.ansi.code_to_chars(code)


def set_title(title: str):
    """
    Set terminal title
    """
    print(colorama.ansi.set_title(title))


class Cursor:
    """
    Provides static methods to control cursor
    """

    @staticmethod
    def print_at(x=1, y=1, text: str = " ", fore="none", style="none", back="none"):
        """
        Print `text` at a specific x and y coordinates
        """
        Cursor.set_position(x, y)
        print(style_text(text, fore=fore, back=back, style=style))

    @staticmethod
    def set_position(x=1, y=1):
        """
        Set the current cursor position to x and y coordinates
        """
        print(colorama.ansi.Cursor.POS(x, y))

    @staticmethod
    def up(n=1):
        """
        Move cursor up by `n`
        """
        print(colorama.ansi.Cursor.UP(n))

    @staticmethod
    def down(n=1):
        """
        Move cursor down by `n`
        """
        print(colorama.ansi.Cursor.DOWN(n))

    @staticmethod
    def left(n=1):
        """
        Move cursor left by `n`
        """
        print(colorama.ansi.Cursor.BACK(n))

    @staticmethod
    def right(n=1):
        """
        Move cursor right by `n`
        """
        print(colorama.ansi.Cursor.FORWARD(n))


def escape(text: str):
    """
    Escape the provided text by formatting it with escape sequences:

    Example:

    ```python
    >>> print(colored_text.escape("{fore_green}Hello{back_red}{reset_fore}World{reset_all}"))
    ```
    """
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
    file=None,
):
    """
    A Convenient copy of print function for colored text. extra arguments added are: `fore`, `back` and `style`
    """
    if file is None:
        file = sys.stdout
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
    """
    A Convenient copy of input function for colored text. extra arguments added are: `fore`, `back` and `style`
    """
    print(prompt, fore=fore, back=back, style=style, end="", flush=True)
    return builtins.input()
