from typing import Union
import numpy as np

# USe dataclas decorator?

class Point():

    def __init__(self, val: Union[np.ndarray, list]):
        if isinstance(val, list):
            val = np.array(val, dtype=np.float16)
        self.val: np.ndarray = val

    @classmethod
    def distance(cls, point_1, point_2) -> float:
        return np.linalg.norm(point_2.val - point_1.val)