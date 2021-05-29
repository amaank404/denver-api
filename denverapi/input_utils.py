"""
Get User input to get file, selection, etc.

This provides some input utilities so you do not need to write them.
"""

import os

__author__ = "Xcodz"
__version__ = "2020.6.4"


def _clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def _print_tree(path):
    dirl = []
    fill = []
    ldir = [x for x in os.listdir(path)]
    for x in ldir:
        if os.path.isdir(os.path.join(path, x)):
            dirl.append(x)
        else:
            fill.append(x)
    dirl.sort()
    fill.sort()
    tp = f"[{path}]\n"
    for x in dirl:
        tp += "\n# " + x
    for x in fill:
        tp += "\n@ " + x
    print(tp)


def get_file_path(mdir=None) -> str:
    """
    makes user select a file using a TUI. `mdir` is the main starting directory which defaults to current
    working directory.

    .. note::
        This clears screen a lot of times and might make your app ugly but
        provides user with a easy way to choose files.
    """
    if mdir is None:
        mdir = os.getcwd()
    mpath = os.path.abspath(mdir)
    while True:
        _print_tree(mpath)
        f = input(">")
        m = os.path.join(mpath, f)
        if os.path.isfile(m):
            _clear()
            return m
        elif os.path.isdir(m):
            mpath = os.path.abspath(m)
            _clear()


def _is_ipv4(ip: str):
    ipp = ip.split(".")
    if len(ipp) != 4:
        return False
    for x in ipp:
        if not x.isnumeric():
            return False
        elif not (int(x) >= 0 or int(x) < 256):
            return False
    return True


def get_ipv4_port(default=("127.0.0.1", "8000")):
    """
    Get a IPv4, port pair. If the user enters invalid info,
    then the defaults are used.
    """
    ipv4 = input(f"IPV4 [{default[0]}] >")
    port = input(f"Port [{default[1]}] >")
    addr = []
    if _is_ipv4(ipv4):
        addr.append(ipv4)
    else:
        print("Invalid IPV4, using default")
        addr.append(default[0])
    if port.isnumeric():
        addr.append(int(port))
    else:
        print("Invalid Port, using default")
        addr.append(default[1])
    return tuple(addr)


if __name__ == "__main__":
    print(get_ipv4_port())
