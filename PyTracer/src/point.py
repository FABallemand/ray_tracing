"""
This module contains the Point class.
"""

from math import sqrt


class Point:
    """
    Class representing a 3D point.
    """

    def __init__(self, x: float, y: float, z: float):
        """
        Initialise Point instance.

        Args:
            x (float): X coordinate.
            y (float): Y coordinate.
            z (float): Z coordinate.
        """
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"Point(x={self.x}, y={self.y}, z={self.z})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    @classmethod
    def distance(cls, point_1: "Point", point_2: "Point") -> float:
        """
        Compute distance between two points.
        """
        if point_1 == point_2:
            return 0.0
        d_x = point_1.x - point_2.x
        d_y = point_1.y - point_2.y
        d_z = point_1.z - point_2.z
        return sqrt(d_x * d_x + d_y * d_y + d_z * d_z)
