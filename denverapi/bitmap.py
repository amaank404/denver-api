__version__ = "2020.6.4"
__author__ = "Xcodz"


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


class BitMap:
    def __init__(self, x, y):
        self.buffer = [[(255, 255, 255) for _ in range(x)] for _ in range(y)]

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


class BitMapPortion(BitMap):
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
