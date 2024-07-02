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
            val = np.array(val, dtype=np.float16)
        self.val: np.ndarray = val

    def __add__(self, other):
        return Color(self.val + other.val)

    def __mul__(self, other):
        if isinstance(other, float):
            return Color(other * self.val)
        else:
            return None # WARNING

BLACK = Color([0., 0., 0.])
WHITE = Color([1., 1., 1.])