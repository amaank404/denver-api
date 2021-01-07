"""
Manipulation of strings to join them
"""

import wcwidth


def join(p1, p2, *p, w=20, **kwargs):
    """
    w is global width of paragraphs
    p1 is the paragraph1
    p2 is the paragraph2
    *p is other paragraphs to join

    in keyword arguments the format is:
        w{para_graph_number}={width}

    in the above way you can specify the default width for paragraphs
    this value is used instead of global w if provided.

    Supports ansi escape sequence and cpic images into the input.
    """
