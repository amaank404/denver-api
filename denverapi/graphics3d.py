from __future__ import annotations

import copy
import math

__version__ = "2020.6.4"
__author__ = "Xcodz"


def flatten(x: float, y: float, z: float, scale: int, distance: int) -> tuple:
    """
    Converts 3d point to a 2d drawable point

    >>> flatten(1, 2, 3, 10, 10)
    (7.6923076923076925, 15.384615384615385)
    """
    projected_x = ((x * distance) / (z + distance)) * scale
    projected_y = ((y * distance) / (z + distance)) * scale
    return projected_x, projected_y


def model_rotate(model, axis, angle) -> list:
    """
    Rotate a model
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
    flatten complete model
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
    rotate a point around a certain axis with a certain angle
    angler can be any integer between 1, 360

    >>> rotate(1, 2, 3, 'y', 90)
    (3.130524675073759, 2, 0.4470070007889556)
    """
    if angle > 360 or angle < 0:
        raise ValueError("Angle is supposed to be in between 0, 360")
    if type(x) is not int:
        raise TypeError("x must be int")
    if type(y) is not int:
        raise TypeError("y must be int")
    if type(z) is not int:
        raise TypeError("z must be int")
    angle = angle / 450 * 180 / math.pi
    if axis == "z":
        newX = x * math.cos(angle) - y * math.sin(angle)
        newY = y * math.cos(angle) + x * math.sin(angle)
        newZ = z
    elif axis == "x":
        newY = y * math.cos(angle) - z * math.sin(angle)
        newZ = z * math.cos(angle) + y * math.sin(angle)
        newX = x
    elif axis == "y":
        newX = x * math.cos(angle) - z * math.sin(angle)
        newZ = z * math.cos(angle) + x * math.sin(angle)
        newY = y
    else:
        raise ValueError("not a valid axis")
    nx = newX
    ny = newY
    nz = newZ
    return nx, ny, nz


class ModelMake:
    def cube(x, y, z, s=1):
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
    with open(model_file, "w") as f:
        for segment in model:
            coord1, coord2 = segment
            f.write("{} {} {}:{} {} {}\n".format(*coord1, *coord2))


def model_load_from_file(model_file):
    f = open(model_file).readlines()
    model = []
    for x in f:
        p1s, p2s = x.split(":", 1)
        p11, p12, p13 = p1s.split(" ", 2)
        p21, p22, p23 = p2s.split(" ", 2)
        p11, p12, p13 = float(p11), float(p12), float(p13)
        p21, p22, p23 = float(p21), float(p22), float(p23)

        n = ((p11, p12, p13), (p21, p22, p23))
        model.append(n)
    return model


def model_viewer(model):
    try:
        import pygame
    except ImportError:
        raise ImportError("Please install 'denver-api[gui-tools]' to use this")

    pygame.init()
    fpsclock = pygame.time.Clock()
    disp = pygame.display.set_mode((600, 400))
    cube3 = model_load_from_file(model)
    rotate = False
    rotate2 = False
    scale = 1
    distance = 10
    r = 1
    r2 = 1
    a = 1
    iskd = False
    gevent = None
    while True:
        if rotate:
            cube3 = model_rotate(cube3, "y", r * a)
            rotate = False
        if rotate2:
            cube3 = model_rotate(cube3, "x", r2 * a)
            rotate2 = False
        cube2 = model_flatten(cube3, scale, distance)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit(0)
            if event.type == pygame.KEYUP:
                iskd = False
            if event.type == pygame.KEYDOWN or iskd:
                iskd = True
                gevent = event
        if iskd and gevent != None:
            if gevent.type == pygame.KEYDOWN:
                event = gevent
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    rotate2 = True
                    if event.key != pygame.K_UP:
                        r2 = 0.2
                    else:
                        r2 = -0.2
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    rotate = True
                    if event.key != pygame.K_LEFT:
                        r = 0.2
                    else:
                        r = -0.2
                elif event.key == pygame.K_a:
                    scale -= 1
                elif event.key == pygame.K_d:
                    scale += 1
                elif event.key == pygame.K_w:
                    distance -= 1
                elif event.key == pygame.K_s:
                    distance += 1
                elif event.key == pygame.K_z:
                    cube3 = model_rotate(cube3, "z", 0.2 * a)
                elif event.key == pygame.K_x:
                    cube3 = model_rotate(cube3, "z", -0.2 * a)
                elif event.key == pygame.K_q:
                    a -= 1
                elif event.key == pygame.K_e:
                    a += 1
        disp.fill((255, 255, 255))

        if distance == 0:
            distance = 1
        for x, y in cube2:
            pygame.draw.aaline(
                disp, (0, 0, 0), (x[0] + 300, x[1] + 200), (y[0] + 300, y[1] + 200)
            )

        pygame.display.update()
        fpsclock.tick(10)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser("graphics3d pygame veiw")
    parser.add_argument("model", metavar="PATH_TO_MODEL", help="PATH TO MODEL")
    args = parser.parse_args()
    model_viewer(args.model)
