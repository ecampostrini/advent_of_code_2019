from typing import NamedTuple

from utils import get_absolute_path


class Point(NamedTuple):
    x: int
    y: int


class Segment(NamedTuple):
    a: Point
    b: Point


def get_point(point: Point, direction, amount) -> Point:
    if direction == "U":
        return Point(point.x, point.y + amount)
    if direction == "R":
        return Point(point.x + amount, point.y)
    if direction == "D":
        return Point(point.x, point.y - amount)
    if direction == "L":
        return Point(point.x - amount, point.y)
    raise RuntimeError("Invalid direction {}".format(direction))


def get_intersect(s1: Segment, s2: Segment):
    horizontal, vertical = (s2, s1) if s1.a.x == s1.b.x else (s1, s2)
    a, b = horizontal.a, horizontal.b
    a, b = (a, b) if a <= b else (b, a)
    c, d = vertical.a, vertical.b
    c, d = (c, d) if c <= d else (d, c)

    if not (a.x <= c.x and a.x <= d.x and c.x <= b.x and d.x <= b.x):
        return None

    if not (c.y <= a.y and c.y <= b.y and a.y <= d.y and b.y <= d.y):
        return None

    return Point(c.x, a.y)


def distance(p: Point):
    return abs(p.x) + abs(p.y)


def get_segments(directions) -> [Segment]:
    previous = Point(0, 0)
    segments = []
    for d in directions:
        current = get_point(previous, d[0], int(d[1:]))
        segments.append(tuple(sorted([current, previous])))
        previous = current
    return segments


def get_segments_and_distance(directions) -> [(Segment, int)]:
    previous = Point(0, 0)
    total_distance = 0
    ret: [(Point, int)] = []
    for d in directions:
        direction, distance = d[0], int(d[1:])
        current = get_point(previous, direction, distance)
        seg = Segment(previous, current)
        ret.append((seg, total_distance))
        total_distance += distance
        previous = current
    return ret


def is_vertical(s: Segment) -> bool:
    a, b = s.a, s.b
    if a.x == b.x:
        return True
    return False


with open(get_absolute_path("day3.input")) as f:
    wire1 = get_segments_and_distance([x.strip()
                                       for x in f.readline().split(",")])
    wire2 = get_segments_and_distance([x.strip()
                                       for x in f.readline().split(",")])

    closest: Point = 9999999
    for (seg1, dist1) in wire1:
        for (seg2, dist2) in wire2:
            intersection = get_intersect(seg1, seg2)
            if intersection is not None and intersection != Point(0, 0):
                distance = dist1 + dist2
                if is_vertical(seg1):
                    distance += abs(intersection.y - seg1.a.y)
                    distance += abs(intersection.x - seg2.a.x)
                else:
                    distance += abs(intersection.y - seg2.a.y)
                    distance += abs(intersection.x - seg1.a.x)
                closest = min(closest, distance)
    print(closest)
