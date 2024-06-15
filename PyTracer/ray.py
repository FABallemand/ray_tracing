
from color import Color, WHITE
from point import Point
from vector import Vector

class Ray():

    def __init__(self, src: Point, dir: Vector, color: Color):
        """
        Light ray

        Parameters
        ----------
        src : Point
            Source
        dir : Vector
            Direction
        color : Color
            Color
        """
        self.src: Point = src
        self.dir: Vector = dir.normalise()
        self.color: color = color

    def __str__(self) -> str:
        return f"Ray(src={self.src}, dir={self.dir}, color={self.color})"

    def follow_ray(self, t: float) -> Point:
        assert t >= 0 # To be improved...
        coord = self.src.coord + t * self.dir.val
        return Point(coord)

    @classmethod
    def from_points(cls, src: Point, point: Point, color: Color = WHITE):
        dir = Vector.from_points(src, point)
        return Ray(src, dir, color)
