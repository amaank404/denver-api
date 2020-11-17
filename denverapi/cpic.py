"""
Colored picture
===============

You can use this module to read, write or print images onto screen, or get printable image.
"""

try:
    from . import ctext
except ImportError:
    import ctext

fore_color = list(ctext.ColoredText.cloredTextEscapeSequenceFore.values())
back_color = list(ctext.ColoredText.cloredTextEscapeSequenceBack.values())
style = list(ctext.ColoredText.styleEscapeSequence.values())
reset = ctext.ColoredText.resetEscapeSequence["all"]


class CImage:
    def __init__(self, image_ascii: str, image_ansi: bytes):
        self.image = image_ascii
        self.image_c = image_ansi


def parse_colors(ansi: bytes) -> list:
    code = []
    for x in range(0, len(ansi), 3):
        fore_color_code = ansi[x]
        back_color_code = ansi[x + 1]
        style_code = ansi[x + 2]
        code.append(
            f"{fore_color[fore_color_code]}{back_color[back_color_code]}{style[style_code]}{{a}}{reset}"
        )
    return code


def combine(image: CImage) -> str:
    text_line = ""
    ansi_code = parse_colors(image.image_c)
    for line in image.image.split("\n"):
        for character in line:
            text_line += ansi_code.pop(0).format(a=character)
        text_line += "\n"
    return text_line


def write_image(image: CImage, file: str) -> None:
    with open(file, "w+b") as writer:
        writer.write(image.image.encode("utf-8"))
        writer.write(b"\0")
        writer.write(image.image_c)


def read_image(file: str) -> CImage:
    with open(file, "r+b") as reader:
        data = reader.read()
    ascii_text, ansi_code = data.split(b"\0", 1)
    ascii_text = ascii_text.decode("utf-8")
    return CImage(ascii_text, ansi_code)


if __name__ == "__main__":

    image_ascii = """+1
234"""

    image_ansi = b"""\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"""

    mi = CImage(image_ascii, image_ansi)
    print(combine(mi))
