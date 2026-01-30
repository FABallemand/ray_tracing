"""
This module contains the Ray class.
"""

from .color import Color
from .point import Point
from .vector import Vector


class Ray:
    """
    Class representing a light ray.
    """

    def __init__(self, src: Point, dir: Vector, color: Color):  # pylint: disable=redefined-builtin
        """
        Initialise Ray instance.

        Note: Normalise direction vector `dir`.

        Args:
            src (Point): Source.
            dir (Vector): Direction.
            color (Color): Color.
        """
        self.src: Point = src
        self.dir: Vector = dir.normalise()
        self.color: Color = color

    def __str__(self) -> str:
        return f"Ray(\n\tsrc={self.src},\n\tdir={self.dir},\n\tcolor={self.color}\n)"

    def follow_ray(self, d: float) -> Point:
        """
        Return the point reached by following the ray for a given
        distance.
        """
        return Point(
            self.src.x + d * self.dir.x,
            self.src.y + d * self.dir.y,
            self.src.z + d * self.dir.z,
        )
