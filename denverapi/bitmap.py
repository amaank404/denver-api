"""
Simple pure python text bitmaps. Something helpful about this is those BitMapPortion.
"""

__version__ = "2020.6.4"
__author__ = "Xcodz"

import abc

Text_To_RgbGrayScale = {
    "0": (0, 0, 0),
    "1": (28, 28, 28),
    "2": (56, 56, 56),
    "3": (85, 85, 85),
    "4": (113, 113, 113),
    "5": (141, 141, 141),
    "6": (170, 170, 170),
    "7": (198, 198, 198),
    "8": (226, 226, 226),
    "9": (255, 255, 255),
}


class BitMapBase(metaclass=abc.ABCMeta):
    pass


class BitMap(BitMapBase):
    """
    A Class for holding a table of text characters.

    Example:

    ```python
    >>> from denverapi import bitmap
    >>> b = bitmap.BitMap(10, 10)
    >>> for x in range(10):
    ...     b[x, 0] = "-"  # Draw a horizontal line at top
    >>> b[0, 9] = "-"*9  # Draw a horizontal line at bottom
    >>> print(b)
    ----------








    ----------
    ```
    """

    def __init__(self, width: int, height: int):
        self.buffer = [[" " for _ in range(width)] for _ in range(height)]

    def __repr__(self):
        return "\n".join(["".join(x) for x in self.buffer])

    def __getitem__(self, i):
        return self.buffer[i[1]][i[0]]

    def __setitem__(self, i, sr):
        ln = sr.split("\n")
        for y in range(len(ln)):
            for x in range(len(ln[y])):
                try:
                    self.buffer[y + i[1]][x + i[0]] = ln[y][x]
                except:
                    pass


class BitMapPortion(BitMapBase):
    """
    A Class to get control of certain areas. Overflow is managed and hidden by default.

    `x` is the x coordinate of starting of the portion<br/>
    `y` is the y coordinate of starting of the portion<br/>
    `w` is the width of the portion<br/>
    `h` is the height of the portion

    It can be used just like regular bitmap object
    """

    def __init__(self, bitmap, x, y, w, h):
        self.bmap = bitmap
        self.x = x
        self.y = y
        self.h = h
        self.w = w

    def __repr__(self):
        portion = self.bmap.buffer[self.y : self.h + self.y]
        for x in range(len(portion)):
            portion[x] = portion[x][self.x : self.x + self.w]
        return "\n".join(["".join(x) for x in portion])

    def __getitem__(self, i):
        return self.bmap[
            self.x + i[0] if i[0] < self.w else self.w + self.x,
            self.y + i[1] if i[1] < self.h else self.h + self.y,
        ]

    def __setitem__(self, i, sr):
        self.bmap[
            self.x + i[0] if i[0] < self.w else self.w + self.x,
            self.y + i[1] if i[1] < self.h else self.h + self.y,
        ] = "\n".join(
            [
                "".join(x)
                for x in [
                    list(xyz[0 : self.w - i[0]])
                    for xyz in sr.split("\n")[0 : self.h - i[1]]
                ]
            ]
        )
