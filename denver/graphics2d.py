"""
Utilities for 2d graphics like degrees between 2 lines.

It uses cartesian coordinates
"""

import math


def get_angle(start_point: tuple, end_point: tuple) -> float:
    dx = end_point[0] - start_point[0]
    dy = end_point[1] - start_point[1]
    rads = math.atan2(-dy, dx)
    rads %= 2 * math.pi
    degrees = math.degrees(rads)
    return degrees


def get_end(start_point: tuple, length: int, rotation: float) -> tuple:
    x = start_point[0] + math.cos(math.radians(rotation)) * length
    y = start_point[1] + math.cos(math.radians(rotation)) * length
    return x, y
