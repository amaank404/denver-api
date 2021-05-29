"""
Data parse

This module provides functionalities for visual
presentation of different data structures.
"""

import csv
import io
from functools import partial
from typing import Callable

ALIGN_CENTER = str.center
ALIGN_RIGHT = str.rjust
ALIGN_LEFT = str.ljust


def format_csv(data: str, align: Callable[[str, int], str] = ALIGN_CENTER) -> str:
    """
    return table formatted csv

    You can also provide `alignment` which should be a function which accepts two arguments,
    one being the string data and the second being the width. for your convenience
    you can use the constants named `ALIGN_CENTER`, `ALIGN_RIGHT`, `ALIGN_LEFT`.

    Example Input:

    ```csv
    Header Name 1,Header Name 2,DataField
    2,ahjf8m,397
    93741,hba,917238
    813u,7634,udd
    ```

    Example output:

    ```
    +===============+===============+===========+
    | Header Name 1 | Header Name 2 | DataField |
    +===============+===============+===========+
    |       2       |     ahjf8m    |    397    |
    +---------------+---------------+-----------+
    |     93741     |      hba      |   917238  |
    +---------------+---------------+-----------+
    |      813u     |      7634     |    udd    |
    +---------------+---------------+-----------+
    ```
    """
    output = io.StringIO()
    print_output = partial(print, file=output)
    reader = csv.reader(data.splitlines())
    rows = list(reader)
    w_cols = [0 for _ in range(len(rows[0]))]
    for row in rows:
        for i in range(len(row)):
            w_cols[i] = max(w_cols[i], len(row[i]))
    headers = rows.pop(0)
    spl_line = "".join([f"+{'='*(x+2)}" for x in w_cols]) + "+"
    print_output(spl_line)
    print_output(
        "| " + (" | ".join([align(x, w) for x, w in zip(headers, w_cols)])) + " |"
    )
    print_output(spl_line)
    spl_line = spl_line.replace("=", "-")
    for row in rows:
        print_output(
            "| " + (" | ".join([align(x, w) for x, w in zip(row, w_cols)])) + " |"
        )
        print_output(spl_line)
    output.seek(0)
    return output.read()[:-1]
