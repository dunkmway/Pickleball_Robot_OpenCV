import numpy as np

class Matrix:
    def __init__(self, arr: np.ndarray) -> None:
        if arr is None or not isinstance(arr, np.ndarray):
            raise TypeError('A matrix must be initialized with a numpy ndarray.')
        if arr.ndim != 2 or not all(len(i) == len(arr[0]) for i in arr):
            raise ValueError('A matrix must be 2 dimensional and rectangular.')

        self.arr = arr
    
    def __str__(self):
        m = len(self.arr)
        mtxStr = ''  
        for i in range(m):
            mtxStr += ('|' + ', '.join( map(lambda x:'{0:8.3f}'.format(x), self.arr[i])) + '| \n')
        return mtxStr
    
    def __add__(self, other):
        # check if other is a matrix
        if not isinstance(other, Matrix):
            raise TypeError('A matrix can only be added to another matrix.')
        # check if the matrices have the same shape.
        # matrices have to be rectangular so shape should work properly
        if self.arr.shape != other.arr.shape:
            raise ValueError('A matrix can only be added to another matrix of the same size.')
        
        return Matrix(self.arr + other.arr)
    
    def __mul__(self, other):
        # check if other is a matrix
        if isinstance(other, Matrix):
            # check if the columns of self is equal to the rows of other
            if self.arr.shape[1] != other.arr.shape[0]:
                raise ValueError('A matrix can only be multiplied to another matrix where the number columns of the first equal the number of rows of the second.')
            
            return Matrix(self.arr @ other.arr)
        
        # check if other is a float or int
        if isinstance(other, (float, int)):
            return Matrix(other * self.arr)
        
        raise TypeError('A matrix can only be multipled by another matrix, a float, or an int.')

    def __rmul__(self, other):
        # matrix multiplication is handled by __mul__

        # check if other is a float or int
        if isinstance(other, (float, int)):
            return self * other
        
        raise TypeError('A matrix can only be multipled by another matrix, a float, or an int.')

    def __pow__(self, other):
        # check if other is a float or int
        if isinstance(other, (float, int)):
            A = self.copy()
            for _ in range(other - 1):
                A = A * self
            return A
            
        raise TypeError('A matrix can only be raised to a power by a float or an int.')






    def norm(self):
        return np.linalg.norm(self.arr)

    def copy(self):
        return Matrix(self.arr.copy())
    



def identity(n: int):
    return Matrix(np.identity(n))

# solves ax = b
def solve(a: Matrix, b: Matrix):
    return Matrix(np.linalg.solve(a.arr, b.arr))