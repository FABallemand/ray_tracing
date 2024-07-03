from typing import Union
import numpy as np

from color import Color
from point import Point
from ray import Ray
from vector import Vector

class Sphere():

    def __init__(self, center: Point, rad: float, color: Color, reflection: float):
        """
        Sphere

        Parameters
        ----------
        center : Point
            Center point
        rad : float
            Radius
        color : Color
            Color
        reflection: float
            Reflection coefficient
        """
        self.center: Point = center
        self.rad: float = rad
        self.color: Color = color
        self.reflection: float = reflection

    def __str__(self) -> str:
        return (f"Sphere(center={self.center}, rad={self.rad}, "
                f"color={self.color}, reflection={self.reflection})")

    def normal_at_point(self, point: Point) -> Vector:
        return Vector.from_points(self.center, point, True)

    def is_point_inside(self, point: Point) -> bool:
        return Point.distance(self.center, point) <= self.rad
    
    def is_ray_above_surface(self, ray: Ray, point: Point) -> bool:
        normal = Vector.from_points(self.center, point, normalise=True)
        point_to_src = Vector.from_points(point, ray.src)
        return Vector.dot_product(normal, point_to_src) > 0
    
    def ray_intersection(self, ray: Ray) -> Union[Point, None]:
        # Ray source inside sphere
        # Not required as we always check if ray is above surface
        # Required when computing reflections??
        if self.is_point_inside(ray.src):
            return None
        
        # Compute intersection
        cs = Vector.from_points(self.center, ray.src)
        dot = Vector.dot_product(ray.dir, cs)
        delta = 4 * dot**2 - 4 * (cs.get_norm()**2 - self.rad**2)
        if delta < 0: # Ray does not intersect sphere
            return None
        elif delta == 0: # Ray tangent to sphere
            return ray.follow_ray(-dot)
        else:
            sqrt_delta = np.sqrt(delta)
            r1 = -2 * dot - sqrt_delta
            r2 = -2 * dot + sqrt_delta
            if r1 < 0 and r2 < 0: # Ray does not intersect sphere
                return None
            else:
                # Ray intersects sphere and is not inside so both solutions are positive
                return ray.follow_ray(min(r1, r2) / 2)
            
    def diffused_color(self, ray: Ray, normal: Vector) -> Color:
        # Check if both vectors normalised ?
        theta = Vector.dot_product(ray.dir, normal)
        color = np.cos(theta) * np.multiply(self.color.val, ray.color.val)
        return Color(color)
    
    def reflected_ray(self, ray: Ray, point: Point) -> Ray:
        reflected_direction = -ray.dir
        return Ray(point, reflected_direction, ray.color)

    @classmethod
    def from_points(cls, center: Point, point: Point):
        rad = Point.distance(center, point)
        return Sphere(center, rad)