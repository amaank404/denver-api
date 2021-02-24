"""
Data Unicode

This module provides with Unicode Data Handling also methods to draw boxes.
Anyone can easily use these unicode data functions until you are working
with a terminal which supports Unicode. It will completely work only if
you have Unicode-13.0.0
"""

__version__ = "2020.6.4"
__author__ = "Xcodz"
shades = [u"\u2591", u"\u2592", u"\u2593", u"\u2588"]

bars = list(u"\u258f\u258e\u258d\u258c\u258b\u258a\u2589")

box = {
    "light box": {
        "/-": u"\u250c-",
        "|": u"\u2502",
        "\\-": u"\u2514-",
        "-/": u"-\u2518",
        "-\\": u"-\u2510",
        "-": u"\u2500",
        "\\/": u"\u2514\u2518",
        "/\\": u"\u250c\u2510",
    },
    "heavy box": {
        "/-": u"\u250f-",
        "\\-": u"\u2517-",
        "-\\": u"-\u2513",
        "-/": u"-\u251b",
        "|": u"\u2503",
        "-": u"\u2501",
        "\\/": u"\u2517\u251b",
        "/\\": u"\u250f\u2513",
    },
    "soft box": {
        "/-": u"\u256d-",
        "|": u"\u2502",
        "\\-": u"\u2570-",
        "-\\": u"-\u256e",
        "-/": u"-\u256f",
        "-": u"\u2500",
        "\\/": u"\u2570\u256f",
        "/\\": u"\u256d\u256e",
    },
}


def convert(text: str, rept: dict):
    x = text
    for k, v in rept.items():
        x = x.replace(k, v)
    return x
