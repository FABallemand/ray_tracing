
from color import Color
from point import Point
from vector import Vector

class Ray():

    def __init__(self, source: Point, direction: Vector, color: Color):
        self.source: Point = source
        self.direction: Vector = direction.normalise()
        self.color: Color = color

    def follow_ray(self, t: float) -> Point:
        assert t >= 0 # To be improved...
        coord = self.source.val + t * self.direction.val
        return Point(coord)

    @classmethod
    def from_points(cls, source: Point, point: Point, color: Color):
        direction = Vector.from_points(source, point)
        return Ray(source, direction, color)
