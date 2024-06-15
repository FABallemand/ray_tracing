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

BLACK = Color([0., 0., 0.])
WHITE = Color([1., 1., 1.])