import os

import numpy as np

from color import Color
from light import Light
from point import Point
from ray import Ray
from scene import Scene
from sphere import Sphere
from vector import Vector

if __name__ == "__main__":
    # Change working directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Create scene
    scene = Scene(view_size=(10, 10), screen_size=(100, 100))

    # Add objects
    sphere_1 = Sphere(Point([0, 0, -1]), 1, Color([1, 0, 0]))
    scene.spheres.append(sphere_1)

    # Add lights
    light_1 = Light(Point([-5, 0, -1]), Color([1, 1, 1]))
    scene.lights.append(light_1)

    # Perform ray-tracing
    scene.ray_trace(Point([0, 0, 1]), Color([0.5, 0.5, 0.5]))

    # Display
    scene.plot()
    
