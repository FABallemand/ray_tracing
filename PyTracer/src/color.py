"""
This module contains the Color class.
"""


class Color:
    """
    Class representing a color.
    """

    def __init__(self, r: float, g: float, b: float):
        """
        Initialise Color instance.

        Args:
            r (float): Red component (between 0 and 1).
            g (float): Green component (between 0 and 1).
            b (float): Blue component (between 0 and 1).
        """
        # Clamp values between 0 and 1
        self.r = max(0, min(r, 1))
        self.g = max(0, min(g, 1))
        self.b = max(0, min(b, 1))

    def __str__(self):
        return f"Color(r={self.r}, g={self.g}, b={self.b})"

    def __add__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)

    def __iadd__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Color(self.r * other, self.g * other, self.b * other)
        if isinstance(other, Color):
            return Color(self.r * other.r, self.g * other.g, self.b * other.b)
        raise ValueError(f"Cannot multiply a Color by object with type : {type(other)}")

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> "Color":
        """
        Create color instance from RGB values.

        Args:
            r (int): Red component (between 0 and 255).
            g (int): Green component (between 0 and 255).
            b (int): Blue component (between 0 and 255).

        Returns:
            Color: Color.
        """
        return Color(r / 255, g / 255, b / 255)


BLACK = Color(0.0, 0.0, 0.0)
WHITE = Color(1.0, 1.0, 1.0)

RED = Color(1.0, 0.0, 0.0)
GREEN = Color(0.0, 1.0, 0.0)
BLUE = Color(0.0, 0.0, 1.0)

DARK_GREY = Color(0.1, 0.1, 0.1)
