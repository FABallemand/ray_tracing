
from color import Color
from point import Point

class Light():

    def __init__(self, position: Point, color: Color):
        self.position: Point = position
        self.color: Color = color