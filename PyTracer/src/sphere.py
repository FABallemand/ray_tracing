"""
This module contains the Sphere class.
"""

from math import cos, sqrt

from .color import Color
from .point import Point
from .ray import Ray
from .vector import Vector


class Sphere:
    """
    Class representing a sphere.
    """

    def __init__(self, center: Point, rad: float, color: Color, reflection: float):
        """
        Initialise a Sphere instance.

        Args:
            center (Point): Center.
            rad (float): Radius.
            color (Color): Diffusion coefficients (i.e.: color).
            reflection (float): Reflection coefficient (between 0 and 1).
        """
        self.center: Point = center
        self.rad: float = rad
        self.color: Color = color
        self.reflection: float = max(
            0, min(reflection, 1)
        )  # Clamp reflection between 0 and 1

    def __str__(self) -> str:
        return (
            f"Sphere(\n\tcenter={self.center},\n\trad={self.rad},"
            f"\n\tcolor={self.color},\n\treflection={self.reflection})"
        )

    def normal_at_point(self, point: Point) -> Vector:
        """
        Return vector perpendicular to the surface of the sphere at a
        given point.
        """
        return Vector.from_points(self.center, point).normalise()

    def is_inside(self, point: Point) -> bool:
        """
        Return `True` if point is inside the sphere, `False` otherwise.
        """
        return Point.distance(self.center, point) <= self.rad

    def is_ray_above_surface(self, ray: Ray, point: Point) -> bool:
        """
        Indicate if a ray is above the sphere surface at a given point.

        Note: This determines if the ray is visible from the point on
        the surface of the sphere.

        Args:
            ray (Ray): Ray.
            point (Point): Point on the surface of the sphere.

        Returns:
            bool: `True` if ray is above the sphere surface at a given
                point, `False` otherwise.
        """
        normal = self.normal_at_point(point)
        point_to_src = Vector.from_points(point, ray.src)
        return Vector.dot_product(normal, point_to_src) > 0

    def ray_intersection(self, ray: Ray) -> Point | None:
        """
        Return the intersection point of a ray and a sphere.

        Note: Return `None` if the source of the ray is inside the sphere.

        Args:
            ray (Ray): Light ray.

        Returns:
            Point | None: Intersection point if it exists, `None`
                otherwise.
        """
        # Handle ray with source inside the sphere
        if self.is_inside(ray.src):
            return None
        # Compute intersections by solving
        # a*t^2 + b*t + c = 0 with a = 1
        # See IPT Centrale 2021, Q7
        center_to_src = Vector.from_points(self.center, ray.src)
        b = 2 * Vector.dot_product(ray.dir, center_to_src)
        c = center_to_src.get_norm() * center_to_src.get_norm() - self.rad * self.rad
        delta = b * b - 4 * c
        if delta < 0:  # Ray does not intersect sphere
            return None
        if delta == 0:  # Ray tangent to sphere
            return ray.follow_ray(-Vector.dot_product(ray.dir, center_to_src))
        sqrt_delta = sqrt(delta)
        r1 = -b - sqrt_delta
        r2 = -b + sqrt_delta
        if r1 < 0 and r2 < 0:  # Ray does not intersect sphere
            return None  # TODO why?
        # Ray intersects sphere
        return ray.follow_ray(min(r1, r2) / 2)

    def diffused_color(self, ray: Ray, normal: Vector) -> Color:
        """
        Return the color of the diffused rays.
        """
        # Both vectors normalised
        return (self.color * ray.color) * cos(Vector.dot_product(ray.dir, normal))

    def reflected_ray(self, ray: Ray, point: Point) -> Ray:
        """
        Create refelected ray from ray hitting the sphere at a given
        point.
        """
        return Ray(point, -ray.dir, ray.color)
