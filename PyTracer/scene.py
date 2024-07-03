from typing import Union
import numpy as np
import matplotlib.pyplot as plt

from color import Color, BLACK, WHITE
from light import Light
from point import Point
from ray import Ray
from sphere import Sphere

class Scene():

    def __init__(self, view_size=(16, 9), screen_size=(1600, 900), nb_max_reflections: int = 3):
        """
        Scene

        Parameters
        ----------
        view_size : tuple, optional
            Size of the view (ie: size of the virtual landscape), by default (16, 9)
        screen_size : tuple, optional
            Siz of the screen (ie: screen resolution), by default (1600, 900)
        """
        self.view_size: tuple[int, int] = view_size
        self.screen_size: tuple[int, int] = screen_size
        self.nb_max_reflections: int = nb_max_reflections
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
        distance_ray_sphere = Point.distance(sphere.center, ray.src)
        for s in self.spheres:
            if s != sphere and Point.distance(s.center, ray.src) < distance_ray_sphere:
                if s.ray_intersection(ray) is not None:
                    return False
        return True
    
    def interception(self, ray: Ray, exception_spheres: list = []) -> tuple[Union[Point, None], Union[Sphere, None]]:
        intersection_point = None
        intersection_distance = None
        intersection_sphere = None
        spheres = [s for s in self.spheres if s not in exception_spheres]
        for sphere in spheres:
            new_intersection_point = sphere.ray_intersection(ray)
            if new_intersection_point is not None:
                new_intersection_distance = Point.distance(new_intersection_point, ray.src)
                if intersection_point is None or new_intersection_distance < intersection_distance:
                    intersection_point = new_intersection_point
                    intersection_distance = new_intersection_distance
                    intersection_sphere = sphere
        return intersection_point, intersection_sphere

    def diffused_color(self, point: Point, sphere: Sphere) -> Color:
        colors = []
        for light in self.lights:
            ray = Ray.from_points(light.position, point, light.color)
            if self.is_ray_visible_from_point(ray, sphere, point):
                colors.append(sphere.diffused_color(ray, sphere.normal_at_point(point)))

        color = BLACK
        for c in colors:
            color += c
        return color
    
    def ray_trace(self, omega: Point, bg_color: Color, lights: bool = False):
        # Iterate over all pixels
        for j in range(self.screen_size[0]):                
            for i in range(self.screen_size[1]):

                # Create ray going through pixel (i,j)
                ray = self.ray_from_pixel(omega, i, j)

                # Compute intersection point and sphere, color pixel accordingly
                intersection_point, intersection_sphere = self.interception(ray)
                if intersection_point is None:
                    self.image[i, j] = bg_color.val
                else:
                    pixel_color = self.diffused_color(intersection_point, intersection_sphere)
                    self.image[i, j] = pixel_color.val

    
    def reflections(self, ray: Ray) -> list[tuple[Point, Sphere]]:
        intersections = [] # Intersections of the (reflected) ray
        exception_spheres = []
        for i in range(self.nb_max_reflections):
            intersection_point, intersection_sphere = self.interception(ray, exception_spheres)
            if intersection_point is None:
                break
            else:
                intersections.append((intersection_point, intersection_sphere))
                ray = intersection_sphere.reflected_ray(ray, intersection_point)
                exception_spheres = [intersection_sphere]
        return intersections
    

    def reflected_color(self, intersections: list[tuple[Point, Sphere]]) -> Color:
        colors = [BLACK] * len(intersections)
        diffused_colors = [self.diffused_color(intersection_point, intersection_sphere)
                           for intersection_point, intersection_sphere in intersections]
        colors[-1] = diffused_colors[-1]
        for i in range(self.nb_max_reflections - 2, -1, -1):
            _, previous_intersection_sphere = intersections[i + 1]
            colors[i] = diffused_colors[i] + previous_intersection_sphere.reflection * diffused_colors[i + 1]
        return colors[0]


    def ray_trace_with_reflection(self, omega: Point, bg_color: Color, lights: bool = False):
        # Iterate over all pixels
        for j in range(self.screen_size[0]):                
            for i in range(self.screen_size[1]):
                # print(f"(i, j) = ({i}, {j})")

                # Create ray going through pixel (i,j)
                ray = self.ray_from_pixel(omega, i, j)

                # Compute intersection point and sphere, color pixel accordingly
                intersections = self.reflections(ray)
                if intersections == []:
                    self.image[i, j] = bg_color.val
                elif len(intersections) == 1:
                    intersection_point, intersection_sphere = intersections[0]
                    pixel_color = self.diffused_color(intersection_point, intersection_sphere)
                    self.image[i, j] = pixel_color.val
                else:
                    pixel_color = self.reflected_color(intersections)
                    self.image[i, j] = pixel_color.val


    def plot(self, path=None):
        plt.figure("PyTracer", figsize=self.view_size)
        plt.imshow(self.image)
        
        if path is not None:
            plt.savefig(path)
        else:
            plt.show()
                