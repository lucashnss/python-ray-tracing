import math
import numpy as np

def create_matrix(a1, a2, a3, a4):
    return np.array([a1, a2, a3, a4])

def affine_transform(vector, transform_type="", x=0, y=0, z=0, angle=0):
    if transform_type == 'translate':
        matrix = translate(x, y, z)
    elif transform_type == 'rotate x':
        matrix = rotate_x(angle)
    elif transform_type == 'rotate y':
        matrix = rotate_y(angle)
    elif transform_type == 'rotate z':
        matrix = rotate_z(angle)
    else:
        print("As transformações aceitas são 'translate', 'rotate_x', 'rotate_y' and 'rotate_z.")

    vector_to_calc = np.append(vector, 1)
    result = np.dot(matrix, vector_to_calc)
    result_to_return = np.array([result[0], result[1], result[2]])
    print(f'{vector} => {result_to_return}')

    return result_to_return

def translate(x:float, y:float, z: float):
    return np.array([[1, 0, 0, x],
                    [0, 1, 0, y],
                    [0, 0, 1, z],
                    [0, 0, 0, 1]])

def rotate_x(angle: float):
    return np.array([[1, 0, 0, 0 ],
                    [0, math.cos(angle), -math.sin(angle), 0],
                    [0, math.sin(angle), math.cos(angle), 0],
                    [0, 0, 0, 1]])

def rotate_y(angle:float):
    return np.array([[math.cos(angle), 0, math.sin(angle), 0],
                    [0, 1, 0, 0],
                    [-math.sin(angle), 0, math.cos(angle), 0],
                    [0, 0, 0, 1]])

def rotate_z(angle: float):
    return np.array([[math.cos(angle), -math.sin(angle), 0, 0],
                    [math.sin(angle), math.cos(angle), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])