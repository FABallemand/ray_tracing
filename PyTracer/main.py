"""
Main file.
"""

import os
import time
import random
from datetime import datetime

from src.color import Color, DARK_GREY, WHITE, RED, BLUE, GREEN
from src.light import Light
from src.point import Point
from src.scene import Scene, SceneWithReflections
from src.sphere import Sphere

SCENE_W = 10
SCENE_H = 10

IMG_W = 2000
IMG_H = 2000


def time_func(f):
    """
    Time function call.
    """
    start = time.time()
    f()
    stop = time.time()
    print(f"Function {f.__name__!r} executed in {(stop - start):.4f} s")


def scene_1(n_max_reflections=0):
    """
    Handle test scene 1.
    """
    # Create scene
    scene = (
        SceneWithReflections(
            (SCENE_W, SCENE_H),
            (IMG_W, IMG_H),
            n_max_reflections,
        )
        if n_max_reflections > 0
        else Scene((SCENE_W, SCENE_H), (IMG_W, IMG_H))
    )

    # Add objects
    scene.spheres = [Sphere(Point(0, 0, -10), 10, BLUE, 0.3)]

    # Add lights
    scene.lights = [
        Light(Point(0, 5, 0), WHITE),
    ]

    # Perform ray-tracing
    scene.ray_trace(Point(0, 0, 1), DARK_GREY)

    # Display
    scene.plot(f"results/scene_1_{n_max_reflections}.png")


def scene_2(n_max_reflections=0):
    """
    Handle test scene 2.
    """
    # Create scene
    scene = (
        SceneWithReflections(
            (SCENE_W, SCENE_H),
            (IMG_W, IMG_H),
            n_max_reflections,
        )
        if n_max_reflections > 0
        else Scene((SCENE_W, SCENE_H), (IMG_W, IMG_H))
    )

    # Add objects
    scene.spheres = [Sphere(Point(0, 0, -10), 10, Color.from_rgb(8, 188, 254), 0.3)]

    # Add lights
    scene.lights = [
        Light(Point(-5, 5, 0), WHITE),
        Light(Point(5, 5, 0), GREEN),
    ]

    # Perform ray-tracing
    scene.ray_trace(Point(0, 0, 1), DARK_GREY)

    # Display
    scene.plot(f"results/scene_2_{n_max_reflections}.png")


def scene_3(n_max_reflections=0):
    """
    Handle test scene 3.
    """
    # Create scene
    scene = (
        SceneWithReflections(
            (SCENE_W, SCENE_H),
            (IMG_W, IMG_H),
            n_max_reflections,
        )
        if n_max_reflections > 0
        else Scene((SCENE_W, SCENE_H), (IMG_W, IMG_H))
    )

    # Add objects
    scene.spheres = [
        Sphere(Point(-10, 0, -10), 8, Color.from_rgb(8, 188, 254), 0.3),
        Sphere(Point(10, 0, -10), 8, Color.from_rgb(8, 8, 255), 0.3),
    ]

    # Add lights
    scene.lights = [
        Light(Point(0, 5, 0), WHITE),
    ]

    # Perform ray-tracing
    scene.ray_trace(Point(0, 0, 1), DARK_GREY)

    # Display
    scene.plot(f"results/scene_3_{n_max_reflections}.png")


def scene_4(n_max_reflections=0):
    """
    Handle test scene 4.
    """
    # Create scene
    scene = (
        SceneWithReflections(
            (SCENE_W, SCENE_H),
            (IMG_W, IMG_H),
            n_max_reflections,
        )
        if n_max_reflections > 0
        else Scene((SCENE_W, SCENE_H), (IMG_W, IMG_H))
    )

    # Add objects
    scene.spheres = [
        Sphere(Point(-10, 0, -10), 8, Color.from_rgb(8, 188, 254), 0.3),
        Sphere(Point(10, 0, -10), 8, Color.from_rgb(8, 8, 255), 0.3),
    ]

    # Add lights
    scene.lights = [
        Light(Point(-5, 5, 0), WHITE),
        Light(Point(5, 5, 0), GREEN),
    ]

    # Perform ray-tracing
    scene.ray_trace(Point(0, 0, 1), DARK_GREY)

    # Display
    scene.plot(f"results/scene_4_{n_max_reflections}.png")


def random_scene(n_max_reflections=0):
    """
    Handle random scenes.
    """
    # Create scene
    scene = (
        SceneWithReflections((SCENE_W, SCENE_H), (IMG_W, IMG_H), n_max_reflections)
        if n_max_reflections > 0
        else Scene((SCENE_W, SCENE_H), (IMG_W, IMG_H))
    )

    min_xy = -50
    min_z = -20

    max_xy = 50
    max_z = -10

    range_size_xy = max_xy - min_xy
    range_size_z = max_z - min_z

    # Add objects
    nb_spheres = 40
    for _ in range(nb_spheres):
        position = Point(
            random.random() * range_size_xy + min_xy,
            random.random() * range_size_xy + min_xy,
            random.random() * range_size_z + min_z,
        )
        size = random.random() * 5 + 1
        color = Color(random.random(), random.random(), random.random())
        reflection = random.random()
        sphere = Sphere(position, size, color, reflection)
        scene.spheres.append(sphere)

    # Add lights
    nb_lights = 3
    for _ in range(nb_lights):
        position = Point(
            random.random() * range_size_xy + min_xy,
            random.random() * range_size_xy + min_xy,
            random.random() * range_size_z + min_z,
        )
        color = Color(random.random(), random.random(), random.random())
        light = Light(position, color)
        scene.lights.append(light)

    # Perform ray-tracing
    # scene.ray_trace(Point([0, 0, 1]), Color([0.5, 0.5, 0.5]))
    scene.ray_trace(Point(0, 0, 1), Color(0.5, 0.5, 0.5))

    # Plot
    scene.plot(
        f"results/scene_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{n_max_reflections}"
    )


if __name__ == "__main__":
    # Change working directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Test
    time_func(scene_1)
    # scene_2(0)
    # scene_3(0)
    # scene_4(0)

    # for i in range(4):
    #     scene_1(i)
    #     scene_2(i)
    #     scene_3(i)
    #     scene_4(i)

    # for _ in range(10):
    #     random_scene()
