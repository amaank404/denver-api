"""
Data parse

This module provides enough functionalities for visual
presentation of data such as dictionaries and lists
"""

__version__ = "2020.6.4"
__author__ = "Xcodz"


import pickle as achar  # achar is pickle in HINDI (India)
import os


# tree printers
def Tree(lis: list, level=0, indent="\t"):
    cx = ""
    for x in lis:
        if type(x) == list:
            cx += Tree(x, level + 1, indent)
        else:
            cx += (indent * level) + x + "\n"
    return cx


def Tree2(lis: list, level=0, indent="  "):
    cx = ""
    for x in lis:
        if type(x) == list:
            cx += Tree2(x, level + 1, indent)
        else:
            cx += (("|" + indent) * level) + "+--" + x + "\n"
    return cx


def Tree3(d: dict, level=0, indent="  "):
    cx = ""
    for k, v in d.items():
        if type(v) == dict:
            if v != {}:
                cx += (("|" + indent) * level) + "+--" + k + "\n"
                cx += Tree3(v, level + 1, indent)
            else:
                cx += (("|" + indent) * level) + "+--" + k + " (EMPTY)\n"
        else:
            cx += (("|" + indent) * level) + "+--" + k + "\n"
    return cx


def StorageTree(Path) -> dict:
    import os

    stor = {}
    for r, d, f in os.walk(Path):
        nr = r[len(Path) + 1 :]
        if len(d) != 0:
            for x in d:
                VSD.mkdir(os.path.join(nr, x).replace(os.sep, "/"), stor)
        if len(f) != 0:
            for x in f:
                VSD.write(os.path.join(nr, x).replace(os.sep, "/"), "File", stor)
    return stor


# Virtual Storage Dictionary
class VSD:
    dic = {}

    def mkdir(path: str, dic: dict = dic):
        cx = ""
        for x in path.split("/"):
            cx += "[" + repr(x) + "]"
        exec("dic" + cx + " = {}")

    def path(path: str, dic: dict = dic):
        cx = ""
        for x in path.split("/"):
            cx += "[" + repr(x) + "]"
        return eval("dic" + cx)

    def write(path: str, data, dic: dict = dic):
        cx = ""
        for x in path.split("/"):
            cx += "[" + repr(x) + "]"
        exec("dic" + cx + " = " + repr(data))

    def delete(path: str, dic: dict = dic):
        cx = ""
        for x in path.split("/"):
            cx += "[" + repr(x) + "]"
        exec("del dic" + cx)

    def dump(dic: dict = dic):
        return achar.dumps(dic)

    def load(data):
        return achar.loads(data)
