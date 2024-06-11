from typing import Union
import numpy as np
import matplotlib.pyplot as plt

from color import Color, BLACK, WHITE
from light import Light
from point import Point
from ray import Ray
from sphere import Sphere

class Scene():

    def __init__(self, view_size=(16, 9), screen_size=(1600, 900)):
        self.view_size: tuple[int, int] = view_size
        self.screen_size: tuple[int, int] = screen_size
        self.image: np.ndarray = np.empty((*screen_size, 3))
        self.lights: list[Light] = []
        self.spheres: list[Sphere] = []

        # Display attributes
        self._center = (self.screen_size[0] / 2, self.screen_size[1] / 2) # Assuming screen size is even
        self._delta_x = self.view_size[0] / self.screen_size[0]
        self._delta_y = self.view_size[1] / self.screen_size[1]

    def pixel_to_point(self, i: int, j: int) -> Point:
        x = (j - self._center[0] + 0.5) * self._delta_x
        y = -(i - self._center[1] + 0.5) * self._delta_y
        return Point(np.array([x, y, 0]))
    
    def ray_from_pixel(self, point: Point, i: int, j: int) -> Ray:
        screen_point = self.pixel_to_point(i, j)
        return Ray.from_points(point, screen_point, BLACK)

    def is_ray_visible_from_point(self, ray: Ray, sphere: Sphere, point: Point) -> bool:
        # Check if ray above surface
        if not sphere.is_ray_above_surface(ray, point):
            return False
        
        # Check if ray not hidden by other sphere
        distance_ray_sphere = Point.distance(sphere.center, ray.source)
        for s in self.spheres:
            if s != sphere and Point.distance(s.center, ray.source) > distance_ray_sphere:
                if s.ray_intersection(ray) is not None:
                    return False
        return True
    
    def interception(self, ray: Ray) -> Union[tuple[Point, int], None]:
        intersection_point = None
        intersection_distance = None
        sphere_idx = -1
        for i, sphere in enumerate(self.spheres):
            new_intersection_point = sphere.ray_intersection(ray)
            if new_intersection_point is not None:
                new_intersection_distance = Point.distance(new_intersection_point, ray.source)
                if intersection_point is None or new_intersection_distance < intersection_distance:
                    intersection_point = new_intersection_point
                    intersection_distance = new_intersection_distance
                    sphere_idx = i
        return intersection_point, sphere_idx

    def diffused_color(self, point: Point, sphere_idx: int) -> Color:
        sphere = self.spheres[sphere_idx]
        colors = []
        for light in self.lights:
            ray = Ray.from_points(light.position, point, light.color)
            if self.is_ray_visible_from_point(ray, sphere, point):
                colors.append(sphere.diffused_color(ray, sphere.normal_at_point(point)))

        color = BLACK
        for c in colors:
            color.val += c.val
        return color
    
    def ray_trace(self, omega: Point, bg_color: Color):
        # Iterate over all pixels
        for j in range(self.screen_size[0]):                
            for i in range(self.screen_size[1]):
                ray = self.ray_from_pixel(omega, i, j)

                intersection_point, sphere_idx = self.interception(ray)
                if intersection_point is not None:
                    pixel_color = self.diffused_color(intersection_point, sphere_idx)
                    self.image[i, j] = pixel_color.val
                else:
                    self.image[i, j] = bg_color.val

    def plot(self, path=None):
        plt.figure("PyTracer", figsize=(16,9))
        plt.imshow(self.image)
        if path is not None:
            plt.savefig(path)
        else:
            plt.show()
                