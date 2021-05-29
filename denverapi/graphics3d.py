"""
Utilities for working with 3d graphics.

for reference model is a List[line: Tuple[start: Tuple(int, int, int), end: Tuple(int, int, int)]].
"""

from __future__ import annotations

import copy
import math

__version__ = "2020.6.4"
__author__ = "Xcodz"


def flatten(x: float, y: float, z: float, scale: int, distance: int) -> tuple:
    """
    Converts 3d point to a 2d drawable point

    ```python
    >>> flatten(1, 2, 3, 10, 10)
    (7.6923076923076925, 15.384615384615385)
    ```
    """
    projected_x = ((x * distance) / (z + distance)) * scale
    projected_y = ((y * distance) / (z + distance)) * scale
    return projected_x, projected_y


def model_rotate(model, axis, angle) -> list:
    """
    Rotate a model.
    """
    d = copy.deepcopy(model)
    for x in range(len(d)):
        p1, p2 = d[x]
        n = (
            rotate(p1[0], p1[1], p1[2], axis, angle),
            rotate(p2[0], p2[1], p2[2], axis, angle),
        )
        d[x] = n
    return d


def model_flatten(model, scale, distance) -> list:
    """
    Flatten a complete model
    """
    d = copy.deepcopy(model)
    for x in range(len(d)):
        p1, p2 = d[x]
        n = (
            flatten(p1[0], p1[1], p1[2], scale, distance),
            flatten(p2[0], p2[1], p2[2], scale, distance),
        )
        d[x] = n
    return d


def rotate(x: int, y: int, z: int, axis: str, angle: int):
    """
    Rotate a point around a certain axis with a certain angle
    angle can be any integer between 1, 360

    ```python
    >>> rotate(1, 2, 3, 'y', 90)
    (3.130524675073759, 2, 0.4470070007889556)
    ```
    """
    angle = angle
    if not isinstance(x, (int, float)):
        raise TypeError("x must be int")
    if not isinstance(y, (int, float)):
        raise TypeError("y must be int")
    if not isinstance(z, (int, float)):
        raise TypeError("z must be int")
    angle = angle / 450 * 180 / math.pi
    if axis == "z":
        new_x = x * math.cos(angle) - y * math.sin(angle)
        new_y = y * math.cos(angle) + x * math.sin(angle)
        new_z = z
    elif axis == "x":
        new_y = y * math.cos(angle) - z * math.sin(angle)
        new_z = z * math.cos(angle) + y * math.sin(angle)
        new_x = x
    elif axis == "y":
        new_x = x * math.cos(angle) - z * math.sin(angle)
        new_z = z * math.cos(angle) + x * math.sin(angle)
        new_y = y
    else:
        raise ValueError("not a valid axis")
    nx = new_x
    ny = new_y
    nz = new_z
    return nx, ny, nz


class ModelMake:
    """
    Provides static methods for creating models of different types of object.
    """

    @staticmethod
    def cube(x, y, z, s=1):
        """
        Create a cube at position `x`, `y`, `z` with size as `s`
        """
        mcube = [
            ((x, y, z), (x + s, y, z)),
            ((x, y, z), (x, y + s, z)),
            ((x, y, z), (x, y, z + s)),
            ((x, y, z + s), (x + s, y, z + s)),
            ((x, y, z + s), (x, y + s, z + s)),
            ((x + s, y, z + s), (x + s, y, z)),
            ((x + s, y, z + s), (x + s, y + s, z + s)),
            ((x + s, y, z), (x + s, y + s, z)),
            ((x, y + s, z + s), (x + s, y + s, z + s)),
            ((x + s, y + s, z + s), (x + s, y + s, z)),
            ((x, y + s, z + s), (x, y + s, z)),
            ((x, y + s, z), (x + s, y + s, z)),
        ]
        return mcube


def model_dump_to_file(model_file, model):
    """
    Write a model to file
    """
    with open(model_file, "w") as f:
        for segment in model:
            coord1, coord2 = segment
            f.write("{} {} {}:{} {} {}\n".format(*coord1, *coord2))


def model_load_from_file(model_file):
    """
    Load a model from file
    """
    f = open(model_file).readlines()
    model = []
    for x in f:
        if x.strip() == "" or x.startswith("#"):
            continue
        x = x.strip()
        p1s, p2s = x.split(":", 1)
        p11, p12, p13 = p1s.split(" ", 2)
        p21, p22, p23 = p2s.split(" ", 2)
        p11, p12, p13 = float(p11), float(p12), float(p13)
        p21, p22, p23 = float(p21), float(p22), float(p23)

        n = ((p11, p12, p13), (p21, p22, p23))
        model.append(n)
    return model
