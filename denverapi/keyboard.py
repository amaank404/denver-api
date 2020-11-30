"""
Cross platform getch implementation and more functions
"""


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
    screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import sys
        import tty

    def __call__(self):
        import sys
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt

        return msvcrt.getch()


_getch = _Getch()

__init__


def getch():
    """
    Cross platform getch (Warning: is doesn't print the character it takes as input, returns bytes)
    """
    return _getch()


def getline(print_new_line=True, *args, **kwargs):
    """
    Cross platform input but it doesn't print the line entered (returns bytes)
    """
    string = b""
    while True:
        s = getch()
        if s == b"\r":
            break
        else:
            string += s
    kwargs["end"] = ""
    print("\n" if print_new_line else "", *args, **kwargs)
    return string
