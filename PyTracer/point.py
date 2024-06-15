from typing import Union
import numpy as np

class Point():

    def __init__(self, coord: Union[np.ndarray, list]):
        """
        3D point

        Parameters
        ----------
        coord : Union[np.ndarray, list]
            Coordinates in three dimensional space
        """
        if isinstance(coord, list):
            coord = np.array(coord, dtype=np.float16)
        self.coord: np.ndarray = coord

    def __str__(self) -> str:
        return f"Point(coord={self.coord})"

    @classmethod
    def distance(cls, point_1, point_2) -> float:
        return np.linalg.norm(point_2.coord - point_1.coord)