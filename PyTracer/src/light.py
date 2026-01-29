"""
This module contains the Light class.
"""

import dataclasses

from .color import Color
from .point import Point


@dataclasses.dataclass
class Light:
    """
    Class representing a light source.
    """

    def __init__(self, position: Point, color: Color):
        """
        Initialise Ligth instance.

        Args:
            position (Point): Position of the light source.
            color (Color): Color of the light source.
        """
        self.position: Point = position
        self.color: Color = color

    def __str__(self):
        return f"Light(\n\tposition={self.position},\n\tcolor={self.color}\n)"
