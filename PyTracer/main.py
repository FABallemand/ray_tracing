import os

import numpy as np

from color import Color
from light import Light
from point import Point
from ray import Ray
from scene import Scene
from sphere import Sphere
from vector import Vector

def scene_1():
    # Create scene
    scene = Scene(view_size=(10, 10), screen_size=(250, 250), nb_max_reflections=3)

    # Add objects
    sphere_1 = Sphere(Point([0, 0, -10]), 5, Color([1, 1, 1]), 0.3)
    scene.spheres.append(sphere_1)

    # Add lights
    light_1 = Light(Point([10, 0, -10]), Color([1, 0, 0]))
    scene.lights.append(light_1)
    light_2 = Light(Point([-10, 0, -10]), Color([0, 0.8, 0]))
    scene.lights.append(light_2)

    # Perform ray-tracing
    scene.ray_trace(Point([0, 0, 1]), Color([0.5, 0.5, 0.5]))
    # scene.ray_trace_with_reflection(Point([0, 0, 1]), Color([0.5, 0.5, 0.5]))

    # Display
    scene.plot()

def scene_2():
    # Create scene
    scene = Scene(view_size=(10, 10), screen_size=(250, 250))

    # Add objects
    sphere_1 = Sphere(Point([0, 0, -10]), 3, Color([1, 0, 0]), 0.1)
    scene.spheres.append(sphere_1)
    sphere_2 = Sphere(Point([0, 20, -10]), 4, Color([0, 1, 0]), 0.2)
    scene.spheres.append(sphere_2)
    sphere_3 = Sphere(Point([20, 0, -10]), 5, Color([0, 0, 1]), 0.3)
    scene.spheres.append(sphere_3)

    # Add lights
    light_1 = Light(Point([0, 0, -1]), Color([1, 1, 1]))
    scene.lights.append(light_1)

    # Perform ray-tracing
    scene.ray_trace(Point([0, 0, 1]), Color([0.5, 0.5, 0.5]))
    # scene.ray_trace_with_reflection(Point([0, 0, 1]), Color([0.5, 0.5, 0.5]))

    # Display
    scene.plot()

if __name__ == "__main__":
    # Change working directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Test
    # scene_1()
    scene_2()
    