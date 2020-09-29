import os
from ..repo_io import json_io, yml_io, pickle_io


class FormatError(Exception):
    pass


def get_format_reader(file: str):
    """
    >>> get_format_reader("file_io.py")
    Traceback (most recent call last):
        ...
    FormatError: File format not supported
    """
    extension = os.path.splitext(file)[1]
    if extension == ".json":
        return json_io
    elif extension == ".yml":
        return yml_io
    elif extension == ".pickle":
        return pickle_io
    else:
        raise FormatError("File format not supported")
