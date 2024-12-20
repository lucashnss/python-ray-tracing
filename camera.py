import numpy as np
from point import Point
from vector import Vector
from ray import Ray
import cv2 as cv

class Camera:
    """Class Representing a Camera in 3D Space
        w is the vector that always points to the center of the screen
        v is the vector that's always points to the right and it's ortogonal to w and up
        u is the vector that's always points up and it's ortogonal to w and v
    Args:
        camera_point: Point, target_point: Point, vector_up: Vector, width: int, height: int
    """

    def __init__(self, camera_point: Point, target_point: Point, vector_up: Vector, width: int, height: int):
        self.camera_point = camera_point # Ponto onde a câmera está.
        self.target_point = target_point # Ponto para onde a câmera está apontando.
        self.vector_up = vector_up # Vetor que aponta para cima.
        self.width = width # Largura da imagem.
        self.height = height    # Altura da imagem.

        self.w = (self.target_point - camera_point).normalize() # Vetor normalizado que aponta para o ponto para onde a câmera está apontando.
        self.v = (self.vector_up.cross_product(self.w)).normalize() # Vetor normalizado que aponta para a direita.
        self.u = (self.w.cross_product(self.v)).normalize() # Vetor normalizado que aponta para cima.

        self.target_distance = self.camera_point.distance(self.target_point) # Distância entre a câmera e o ponto para onde ela está apontando.


    def ray_casting(self, entities, depth):
        """Ray Casting Method"""

        image = np.zeros((self.width, self.height, 3), dtype=np.uint8) # Cria uma imagem preta.


        for i in range(self.height):
            for j in range(self.width):
                print(  self.w.scale(depth) +
                        self.v.scale(2 * 0.5 * (j / self.height - 0.5)) +
                        self.u.scale(2 * 0.5 * (i / self.width - 0.5)))

                image[i,j]= (251,198,207)


        cv.imshow("image", image)
        cv.waitKey(0)
        cv.destroyAllWindows("i")

    def __str__(self):
        return f"Camera Point: {self.camera_point}, Target Point: {self.target_point}, Vector Up: {self.vector_up}, Width: {self.width}, Height: {self.height}, W: {self.w}, V: {self.v}, U: {self.u}, Target Distance: {self.target_distance}"
