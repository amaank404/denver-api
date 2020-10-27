"""
Raw Data

A Module for struct module for making formats
and use them directly or by conversion
"""

import struct

__version__ = "2020.6.4"
__author__ = "Xcodz"

pack_format = {
    "i8": "b",
    "iu8": "B",
    "i16": "h",
    "iu16": "H",
    "i32": "i",
    "iu32": "I",
    "i64": "l",
    "iu64": "L",
    "i128": "q",
    "iu128": "Q",
    "f16": "e",
    "f32": "f",
    "f64": "d",
    "c": "c",
    "b": "?",
}


def make_struct_format(format: list):
    d = "<"
    for x in format:
        d += pack_format[x]
    return d


def pack(fmt, *objs):
    return struct.pack(make_struct_format(fmt), *objs)


def unpack(fmt, bytstr: bytes):
    return struct.unpack(make_struct_format(fmt), bytstr)


def calc_size(fmt):
    return struct.calcsize(make_struct_format(fmt))


def main():
    fmt = ["i8", "i8", "b", "c"]
    obj = (123, 12, True, b"a")

    fmts = make_struct_format(fmt)
    pf = struct.pack(fmts, *obj)

    d = unpack(("iu32",), b"\xca\x0d\0\0")

    print(fmt, obj, fmts, pf, d, sep="\n")


if __name__ == "__main__":
    main()
