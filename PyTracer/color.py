from typing import Union
import numpy as np

class Color():

    def __init__(self, val: Union[np.ndarray, list]):
        """
        Color

        Parameters
        ----------
        val : Union[np.ndarray, list]
            Value
        """
        if isinstance(val, list):
            val = np.array(val, dtype=np.float32)
        self.val: np.ndarray = val

    def __str__(self):
        return f"Color(val={self.val})"

    def __add__(self, other):
        return Color(self.val + other.val)
    
    def __iadd__(self, other):
        return Color(self.val + other.val)

    def __mul__(self, other):
        if isinstance(other, float):
            return Color(other * self.val)
        else:
            return None # WARNING

BLACK = Color([0., 0., 0.])
WHITE = Color([1., 1., 1.])
RED = Color([1., 0., 0.])
GREEN = Color([0., 1., 0.])
BLUE = Color([0., 0., 1.])