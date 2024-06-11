from typing import Union
import numpy as np

from point import Point

class Vector():

    def __init__(self, val: Union[np.ndarray, list]):
        if isinstance(val, list):
            val = np.array(val, dtype=np.float16)
        self.val: np.ndarray = val

    def __neg__(self):
        return Vector(-self.val)

    def get_norm(self) -> float:
        return np.linalg.norm(self.val)

    def normalise(self):
        norm = self.get_norm()
        if norm != 0:
            self.val /= norm
        return self

    @classmethod
    def from_points(cls, start: Point, stop: Point, normalise: bool = False):
        v = Vector(stop.val - start.val)
        if normalise:
            v.normalise()
        return v
    
    @classmethod
    def dot_product(cls, a, b):
        return np.dot(a.val, b.val)
