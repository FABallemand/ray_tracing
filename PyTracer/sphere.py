from typing import Union
import numpy as np

from color import Color
from point import Point
from ray import Ray
from vector import Vector

class Sphere():

    def __init__(self, center: Point, radius: float, color: Color):
        self.center: Point = center
        self.radius: float = radius
        self.color: Color = color

    def normal_at_point(self, point: Point) -> Vector:
        return Vector.from_points(self.center, point, True)

    def is_point_inside(self, point: Point) -> bool:
        return Point.distance(self.center, point) <= self.radius
    
    def is_ray_above_surface(self, ray: Ray, point: Point) -> bool:
        normal = Vector.from_points(self.center, point, normalise=True) # Vector normal to plane tangent to sphere in point
        point_to_ray = Vector.from_points(point, ray.source) # Vector from point to ray source
        return Vector.dot_product(normal, point_to_ray) > 0
    
    def ray_intersection(self, ray: Ray) -> Union[Point, None]:
        # Ray source inside sphere
        if self.is_point_inside(ray.source):
            return None
        
        # Compute intersection
        ac = Vector.from_points(self.center, ray.source)
        dot = Vector.dot_product(ray.direction, ac)
        delta = 4 * dot**2 - 4 * (ac.get_norm()**2 - self.radius**2)
        if delta < 0: # ray does not intersect sphere
            return None
        elif delta == 0: # ray tangent to sphere
            return ray.follow_ray(-dot)
        else:
            sqrt_delta = np.sqrt(delta)
            r1 = -2 * dot - sqrt_delta
            r2 = -2 * dot + sqrt_delta
            if r1 < 0 and r2 < 0: # ray does not intersect sphere
                return None
            else:
                # ray intersects sphere and is not inside so both solutions are positive
                return ray.follow_ray(min(r1, r2) / 2)
            
    def diffused_color(self, ray: Ray, normal: Vector) -> Color:
        # Check if both vectors normalised ?
        theta = Vector.dot_product(ray.direction, normal)
        color = np.cos(theta) * np.multiply(self.color.val, ray.color.val)
        return Color(color)
    
    def reflected_ray(self, ray: Ray, point: Point) -> Ray:
        reflected_direction = Vector(-ray.direction.val)
        return Ray(point, reflected_direction, ray.color) # Change color

    @classmethod
    def from_points(cls, center: Point, point: Point):
        radius = Point.distance(center, point)
        return Sphere(center, radius)