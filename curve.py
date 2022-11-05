from typing import Sequence


def interpolate(p1: Sequence, p2: Sequence, t: float):
    return [(1 - t) * p1[i] + t * p2[i] for i in range(2)]


def get_curve_point(vertexes: Sequence, r: int, i: int, t: float):
    if r == 0:
        return vertexes[i]

    return interpolate(get_curve_point(vertexes, r - 1, i, t), get_curve_point(vertexes, r - 1, i + 1, t), t)


def generate_curve(vertexes: Sequence, density=100):
    points = []

    if len(vertexes) <= 1:
        return points

    for i in range(density):
        points.append(get_curve_point(vertexes, len(vertexes) - 1, 0, i / density))

    return points


__all__ = 'interpolate', 'get_curve_point', 'generate_curve'
