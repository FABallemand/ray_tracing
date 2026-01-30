"""
This module contains the Scene class.
"""

from typing import override

import matplotlib.pyplot as plt

from .color import BLACK, Color
from .light import Light
from .point import Point
from .ray import Ray
from .sphere import Sphere
from .vector import Vector


class Scene:
    """
    Class representing a scene.
    """

    def __init__(
        self,
        view_size: tuple[int, int] = (16, 9),
        screen_size: tuple[int, int] = (1600, 900),
    ):
        """
        Initialise a Scene instance.

        Args:
            view_size (tuple[int, int], optional): Size of the view
                (i.e.: size of the virtual landscape). Defaults to
                (16, 9).
            screen_size (tuple[int, int], optional): Size of the screen
                (i.e.: screen resolution). Defaults to (1600, 900).
        """
        self.view_size: tuple[int, int] = view_size
        self.screen_size: tuple[int, int] = screen_size
        self.image: list[list[list[float]]] = [
            [[0, 0, 0] for _ in range(self.screen_size[0])]
            for _ in range(self.screen_size[1])
        ]
        self.lights: list[Light] = []
        self.spheres: list[Sphere] = []

        # Display attributes
        self._center = (
            self.screen_size[0] / 2,
            self.screen_size[1] / 2,
        )  # Assuming screen size is even
        self._delta_x = (
            self.view_size[0] / self.screen_size[0]
        )  # Horizontal space covered by a pixel
        self._delta_y = (
            self.view_size[1] / self.screen_size[1]
        )  # Vertical space covered by a pixel

    def set_pixel_color(self, i: int, j: int, color: Color):
        """
        Set the color of a given pixel.

        Args:
            i (int): Pixel row coordinate.
            j (int): Pixel column coordinate.
            color (Color): Color.
        """
        self.image[i][j][0] = color.r
        self.image[i][j][1] = color.g
        self.image[i][j][2] = color.b

    def pixel_to_point(self, i: int, j: int) -> Point:
        """
        Convert pixel coordinates to point.

        Note: Transform pixel coordinates to scene coordinates.

        Args:
            i (int): Pixel row coordinate.
            j (int): Pixel column coordinate.

        Returns:
            Point: Point corresponding to the pixel.
        """
        x = (j - self._center[0] + 0.5) * self._delta_x
        y = -(i - self._center[1] + 0.5) * self._delta_y
        return Point(x, y, 0)  # The screen is located on the plane z = 0

    def ray_from_pixel(self, omega: Point, i: int, j: int) -> Ray:
        """
        Create ray from pixel.

        Args:
            omega (Point): Observation point.
            i (int): Pixel row coordinate.
            j (int): Pixel column coordinate.

        Returns:
            Ray: Ray from pixel.
        """
        screen_point = self.pixel_to_point(i, j)
        return Ray(omega, Vector.from_points(omega, screen_point), BLACK)

    def is_ray_visible_from_point(self, ray: Ray, sphere: Sphere, point: Point) -> bool:
        """
        Indicate if a ray is visible from a given point on the surface of the sphere.

        Args:
            ray (Ray): Ray.
            sphere (Sphere): Sphere.
            point (Point): Point on the surface of the sphere.

        Returns:
            bool: `True` if the ray is visible, `False` otherwise.
        """
        # Check if ray above surface
        if not sphere.is_ray_above_surface(ray, point):
            return False

        # Check if ray not hidden by other sphere
        dst = Point.distance(sphere.center, ray.src)
        for s in self.spheres:
            if s != sphere and Point.distance(s.center, ray.src) < dst:
                if s.ray_intersection(ray) is not None:
                    return False
        return True

    def interception(
        self, ray: Ray, exception_spheres: list = None
    ) -> tuple[Point | None, Sphere | None]:
        """
        Compute the first material point reached by a ligth ray in the scene.

        Args:
            ray (Ray): Ray.
            exception_spheres (list, optional): List of spheres to
                ignore. Defaults to None.

        Returns:
            tuple[Point | None, Sphere | None]: Point and corresponding
                sphere reached if the ray intercept an object,
                (`None`, `None`) otherwise.
        """
        exception_spheres = [] if exception_spheres is None else exception_spheres
        intersection_point = None
        intersection_distance = None
        intersection_sphere = None
        for sphere in [s for s in self.spheres if s not in exception_spheres]:
            new_intersection_point = sphere.ray_intersection(ray)
            if new_intersection_point is not None:
                new_intersection_distance = Point.distance(
                    new_intersection_point, ray.src
                )
                if (
                    intersection_point is None
                    or new_intersection_distance < intersection_distance
                ):
                    intersection_point = new_intersection_point
                    intersection_distance = new_intersection_distance
                    intersection_sphere = sphere
        return intersection_point, intersection_sphere

    def diffused_color(self, point: Point, sphere: Sphere) -> Color:
        """
        Return the color diffused by a given point on the surface of a sphere.

        Args:
            point (Point): Point on the surface of a sphere.
            sphere (Sphere): Sphere.

        Returns:
            Color: Color diffused by the point.
        """
        colors = []
        for light in self.lights:
            ray = Ray(
                light.position, Vector.from_points(light.position, point), light.color
            )
            if self.is_ray_visible_from_point(ray, sphere, point):
                colors.append(sphere.diffused_color(ray, sphere.normal_at_point(point)))
        return sum(colors, start=BLACK)

    def ray_trace(self, omega: Point, bg_color: Color):
        """
        Generate image of the scene with ray tracing.

        Args:
            omega (Point): Observation point.
            bg_color (Color): Background color.
        """
        # Iterate over all pixels
        for j in range(self.screen_size[0]):
            for i in range(self.screen_size[1]):
                # Create ray going through pixel (i,j)
                ray = self.ray_from_pixel(omega, i, j)
                # Compute intersection point and sphere, and color pixel accordingly
                intersection_point, intersection_sphere = self.interception(ray)
                if intersection_point is None:
                    self.set_pixel_color(i, j, bg_color)
                else:
                    self.set_pixel_color(
                        i,
                        j,
                        self.diffused_color(intersection_point, intersection_sphere),
                    )

    def plot(self, path: str = None):  # TODO handle path properly
        """
        Plot scene.

        Args:
            path (str, optional): Path to the result image. Defaults
            to None.
        """
        plt.figure("PyTracer", figsize=self.view_size)
        plt.imshow(self.image)
        if path is None:
            plt.show()
        else:
            plt.savefig(path)


class SceneWithReflections(Scene):
    """
    Class representing a scene (with light reflections).
    """

    def __init__(
        self,
        view_size: tuple[int, int] = (16, 9),
        screen_size: tuple[int, int] = (1600, 900),
        n_max_reflections: int = 3,
    ):
        """
        Initialise a SceneWithReflections instance.

        Args:
            view_size (tuple[int, int], optional): Size of the view
                (i.e.: size of the virtual landscape). Defaults to
                (16, 9).
            screen_size (tuple[int, int], optional): Size of the screen
                (i.e.: screen resolution). Defaults to (1600, 900).
            n_max_reflections (int, optional): Maximum number of light
                rays reflections. Defaults to 3.
        """
        super().__init__(view_size, screen_size)
        self.n_max_reflections: int = n_max_reflections

    def reflections(self, ray: Ray) -> list[tuple[Point, Sphere]]:
        """
        Compute the successive material points reached by a light ray
        over reflections.

        Args:
            ray (Ray): Ray.

        Returns:
            list[tuple[Point, Sphere]]: List of point and corresponding
                spheres reached by a ray and its reflections.
        """
        intersections = []  # Intersections of the (reflected) ray
        exception_spheres = []
        for _ in range(self.n_max_reflections):
            intersection_point, intersection_sphere = self.interception(
                ray, exception_spheres
            )
            if intersection_point is None:
                break
            intersections.append((intersection_point, intersection_sphere))
            ray = intersection_sphere.reflected_ray(ray, intersection_point)
            # Do not consider the current intersection sphere for the next intersection
            # search as the ray starts *on* this sphere
            exception_spheres = [intersection_sphere]
        return intersections

    def reflected_color(self, intersections: list[tuple[Point, Sphere]]) -> Color:
        """
        Compute the reflected color given a list of points and
        corresponding spheres corresponding to the successive reflections.

        Args:
            intersections (list[tuple[Point, Sphere]]): List of point
                and corresponding spheres reached by a ray and its
                reflections.

        Returns:
            Color: Color of the first point reached.
        """
        colors = [BLACK] * len(intersections)
        diffused_colors = [
            self.diffused_color(intersection_point, intersection_sphere)
            for intersection_point, intersection_sphere in intersections
        ]
        colors[-1] = diffused_colors[-1]  # Last object is not subject to reflection
        for i in range(self.n_max_reflections - 2, -1, -1):
            _, previous_intersection_sphere = intersections[i + 1]
            colors[i] = (
                diffused_colors[i]
                + previous_intersection_sphere.reflection * colors[i + 1]
            )
        return colors[0]  # Color of the first point reached

    @override  # Override parent class method to handle reflections
    def ray_trace(self, omega: Point, bg_color: Color):
        """
        Generate image of the scene with ray tracing (with light
        reflections).

        Args:
            omega (Point): Observation point.
            bg_color (Color): Background color.
        """
        # Iterate over all pixels
        for j in range(self.screen_size[0]):
            for i in range(self.screen_size[1]):
                # Create ray going through pixel (i,j)
                ray = self.ray_from_pixel(omega, i, j)
                # Compute intersection point and sphere, and color pixel accordingly
                intersections = self.reflections(ray)
                if not intersections:
                    self.set_pixel_color(i, j, bg_color)
                elif len(intersections) == 1:
                    intersection_point, intersection_sphere = intersections[0]
                    self.set_pixel_color(
                        i,
                        j,
                        self.diffused_color(intersection_point, intersection_sphere),
                    )
                else:
                    self.set_pixel_color(i, j, self.reflected_color(intersections))
