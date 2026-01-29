"""
This module contains the Vector class.
"""

from math import sqrt

from .point import Point


class Vector:
    """
    Class representing a 3D vector.
    """

    def __init__(self, x: float, y: float, z: float):
        """
        Initialise Vector instance.

        Args:
            x (float): X coordinate.
            y (float): Y coordinate.
            z (float): Z coordinate.
        """
        self.x = x
        self.y = y
        self.z = z
        self._norm = None

    def __str__(self) -> str:
        return f"Vector(x={self.x}, y={self.y}, z={self.z})"

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def get_norm(self) -> float:
        """
        Return the norm of the vector.
        """
        if self._norm is None:
            self._norm = sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        return self._norm

    def normalise(self):
        """
        Normalise vector.
        """
        norm = self.get_norm()
        if norm > 0:
            self.x /= norm
            self.y /= norm
            self.z /= norm
            self._norm = 1
        return self

    @classmethod
    def from_points(cls, start: Point, stop: Point) -> "Vector":
        """
        Create vector from two points.
        """
        return Vector(stop.x - start.x, stop.y - start.y, stop.z - start.z)

    @classmethod
    def dot_product(cls, a: "Vector", b: "Vector") -> float:
        """
        Compute the dot product between two vectors.
        """
        return a.x * b.x + a.y * b.y + a.z * b.z
