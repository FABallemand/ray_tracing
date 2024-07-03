import os

import numpy as np

from color import Color, BLACK, WHITE, RED, GREEN, BLUE
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
    sphere_1 = Sphere(Point([0, 0, -10]), 5, WHITE, 0.3)
    scene.spheres.append(sphere_1)

    # Add lights
    light_1 = Light(Point([10, 0, -10]), BLUE)
    scene.lights.append(light_1)
    light_2 = Light(Point([-10, 0, -10]), BLUE)
    scene.lights.append(light_2)
    light_3 = Light(Point([0, 10, -5]), RED)
    scene.lights.append(light_3)
    light_4 = Light(Point([0, -10, -5]), GREEN)
    scene.lights.append(light_4)

    # Perform ray-tracing
    # scene.ray_trace(Point([0, 0, 1]), Color([0.5, 0.5, 0.5]))
    scene.ray_trace_with_reflection(Point([0, 0, 1]), Color([0.5, 0.5, 0.5]))

    # Display
    scene.plot("scene_1.png")

def scene_2():
    # Create scene
    scene = Scene(view_size=(10, 10), screen_size=(250, 250))

    # Add objects
    sphere_1 = Sphere(Point([-20, 0, -10]), 3, RED, 0.1)
    scene.spheres.append(sphere_1)
    sphere_2 = Sphere(Point([0, 20, -10]), 4, GREEN, 0.2)
    scene.spheres.append(sphere_2)
    sphere_3 = Sphere(Point([20, 0, -10]), 5, BLUE, 0.3)
    scene.spheres.append(sphere_3)

    # Add lights
    light_1 = Light(Point([0, 0, -5]), WHITE)
    scene.lights.append(light_1)

    # Perform ray-tracing
    # scene.ray_trace(Point([0, 0, 1]), Color([0.5, 0.5, 0.5]))
    scene.ray_trace_with_reflection(Point([0, 0, 1]), Color([0.5, 0.5, 0.5]))

    # Display
    scene.plot("scene_2.png")

def scene_3():
    # Create scene
    scene = Scene(view_size=(10, 10), screen_size=(250, 250))

    # Add objects
    sphere_1 = Sphere(Point([-20, 0, -10]), 2, RED, 0.5)
    scene.spheres.append(sphere_1)
    sphere_2 = Sphere(Point([-40, 0, -10]), 4, RED, 0.5)
    scene.spheres.append(sphere_2)
    sphere_3 = Sphere(Point([-5, 20, -10]), 5, GREEN, 0.5)
    scene.spheres.append(sphere_3)
    sphere_4 = Sphere(Point([5, 20, -10]), 5, GREEN, 0.5)
    scene.spheres.append(sphere_4)
    sphere_5 = Sphere(Point([20, 0, -10]), 4, BLUE, 0.5)
    scene.spheres.append(sphere_5)
    sphere_6 = Sphere(Point([40, 0, -10]), 2, BLUE, 0.5)
    scene.spheres.append(sphere_6)
    sphere_7 = Sphere(Point([0, -20, -15]), 4, RED + GREEN, 0.5)
    scene.spheres.append(sphere_7)
    sphere_8 = Sphere(Point([0, -40, -10]), 5, RED + GREEN, 0.5)
    scene.spheres.append(sphere_8)

    # Add lights
    light_1 = Light(Point([0, 0, -10]), WHITE)
    scene.lights.append(light_1)

    # Perform ray-tracing
    # scene.ray_trace(Point([0, 0, 1]), Color([0.5, 0.5, 0.5]))
    scene.ray_trace_with_reflection(Point([0, 0, 1]), Color([0.5, 0.5, 0.5]))

    # Display
    scene.plot("scene_3.png")

def random_scene():
    # Create scene
    scene = Scene(view_size=(10, 10), screen_size=(250, 250))

    min = np.array([-50, -50, -20])
    max = np.array([50, 50, -10])
    range_size = max - min

    # Add objects
    nb_spheres = 40
    for _ in range(nb_spheres):
        position = Point(np.random.random(3) * range_size + min)
        size = np.random.random() * 5 + 1
        color = Color(np.random.random(3))
        reflection = np.random.random()
        sphere = Sphere(position, size, color, reflection)
        scene.spheres.append(sphere)

    # Add lights
    nb_lights = 3
    for _ in range(nb_lights):
        position = Point(np.random.random(3) * range_size + min)
        color = Color(np.random.random(3))
        light = Light(position, color)
        scene.lights.append(light)

    # Perform ray-tracing
    # scene.ray_trace(Point([0, 0, 1]), Color([0.5, 0.5, 0.5]))
    scene.ray_trace_with_reflection(Point([0, 0, 1]), Color([0.5, 0.5, 0.5]))

    # Display
    from datetime import datetime
    timestamp = datetime.now()
    path = f"scene_{timestamp.strftime('%Y%m%d_%H%M%S')}"
    scene.plot(path)

if __name__ == "__main__":
    # Change working directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Test
    # scene_1()
    # scene_2()
    # scene_3()
    for _ in range(10):
        random_scene()
    