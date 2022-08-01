import numpy as np
from matrix_def import Matrix


class Vector(Matrix):
    def __init__(self, arr: np.ndarray) -> None:
        if arr is None or not isinstance(arr, np.ndarray):
            raise TypeError('A vector must be initialized with a numpy ndarray.')
        if arr.shape[0] != 1 and arr.shape[1] != 1:
            ValueError('Vectors must have 1 row or 1 column.')
        super().__init__(arr)

    def normalize(self):
        return Vector((1 / self.norm()) * self.arr)

def dot(a: Vector, b: Vector):
    return Vector(np.vdot(a.arr, b.arr))

def cross(a: Vector, b: Vector):
    return Vector(np.cross(a.arr, b.arr))
