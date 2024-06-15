from typing import Union
import numpy as np

from point import Point

class Vector():

    def __init__(self, val: Union[np.ndarray, list]):
        """
        3D vector

        Parameters
        ----------
        val : Union[np.ndarray, list]
            Value in three dimensional space
        """
        if isinstance(val, list):
            val = np.array(val, dtype=np.float16)
        self.val: np.ndarray = val

        self._norm = None

    def __str__(self) -> str:
        return f"Vector(val={self.val})"

    def __neg__(self):
        return Vector(-self.val)
    
    def __add__(self, other):
        return Vector(self.val + other.val)
    
    def __sub__(self, other):
        return Vector(self.val - other.val)

    def get_norm(self) -> float:
        # if self._norm is None:
        #     self._norm = np.linalg.norm(self.val)
        # return self._norm
        return np.linalg.norm(self.val) # Test best implementation

    def normalise(self):
        norm = self.get_norm()
        if norm != 0:
            self.val /= norm
        return self

    @classmethod
    def from_points(cls, start: Point, stop: Point, normalise: bool = False):
        v = Vector(stop.coord - start.coord)
        if normalise:
            v.normalise()
        return v
    
    @classmethod
    def dot_product(cls, a, b):
        return np.dot(a.val, b.val)
