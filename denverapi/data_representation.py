"""
Data parse

This module provides enough functionalities for visual
presentation of data such as dictionaries and lists
"""

__version__ = "2021.2.24"
__author__ = "Xcodz"


# tree printers
def tree(lis: list, level=0, indent="\t"):
    cx = ""
    for x in lis:
        if type(x) == list:
            cx += tree(x, level + 1, indent)
        else:
            cx += (indent * level) + x + "\n"
    return cx


def tree2(lis: list, level=0, indent="  "):
    cx = ""
    for x in lis:
        if type(x) == list:
            cx += tree2(x, level + 1, indent)
        else:
            cx += (("|" + indent) * level) + "+--" + x + "\n"
    return cx


def tree3(d: dict, level=0, indent="  "):
    cx = ""
    for k, v in d.items():
        if type(v) == dict:
            if v != {}:
                cx += (("|" + indent) * level) + "+--" + k + "\n"
                cx += tree3(v, level + 1, indent)
            else:
                cx += (("|" + indent) * level) + "+--" + k + " (EMPTY)\n"
        else:
            cx += (("|" + indent) * level) + "+--" + k + "\n"
    return cx
