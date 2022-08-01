import numpy as np
import matrix_def as vector
from vector_def import Vector

import matrix_def as matrix
from matrix_def import Matrix

class Camera:
    def __init__(self, id, posX=0.0, posY=0.0, posZ=0.0, normalX=0.0, normalY=0.0, normalZ=1.0, upX=0.0, upY=1.0, upZ=0.0):
        self.id = id
        self.pos = Vector(np.array([[posX], [posY], [posZ]]))
        self.normal = Vector(np.array([[normalX], [normalY], [normalZ]])).normalize()
        self.up = Vector(np.array([[upX], [upY], [upZ]])).normalize()
        self.transformation_matrix = Matrix(np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]))
    
    def __str__(self) -> str:
        string = ''
        string += '---------- Camera ----------\n'
        string += 'ID: ' + self.id + '\n'
        string += 'Pos: \n' + str(self.pos) + '\n'
        string += 'Normal: \n' + str(self.normal) + '\n'
        string += 'Up: \n' + str(self.up) + '\n'
        string += 'Transformation Matrix:\n' + str(self.transformation_matrix) + '\n'
        string += '----------------------------'
        return string

    
