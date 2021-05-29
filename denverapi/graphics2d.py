"""
Utilities for 2d graphics.

It uses cartesian coordinates
"""

import math


def get_angle(start_point: tuple, end_point: tuple) -> float:
    """
    Determines the angle between the line specified by `start_point` and `end_point`.
    """
    dx = end_point[0] - start_point[0]
    dy = end_point[1] - start_point[1]
    rads = math.atan2(-dy, dx)
    rads %= 2 * math.pi
    degrees = math.degrees(rads)
    return degrees


def get_end(start_point: tuple, length: int, rotation: float) -> tuple:
    """
    Get the end of a line `length` units long from `start_point` and angle dtermined by given `rotation`.
    """
    x = start_point[0] + math.cos(math.radians(rotation)) * length
    y = start_point[1] + math.cos(math.radians(rotation)) * length
    return x, y
