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

    def __init__(self, camera_point: Point, target_point: Point, vector_up: Vector, hres: int, vres: int):
        self.camera_point = camera_point # Ponto onde a câmera está.
        self.target_point = target_point # Ponto para onde a câmera está apontando.
        self.vector_up = vector_up # Vetor que aponta para cima.
        self.hres = hres      # Largura da imagem.
        self.vres = vres    # Altura da imagem.

        self.w = (self.target_point - camera_point).normalize() # Vetor normalizado que aponta para o ponto para onde a câmera está apontando.
        self.v = (self.vector_up.cross_product(self.w)).normalize() # Vetor normalizado que aponta para a direita.
        self.u = (self.w.cross_product(self.v)).normalize() # Vetor normalizado que aponta para cima.

        self.target_distance = self.camera_point.distance(self.target_point) # Distância entre a câmera e o ponto para onde ela está apontando.

    def __str__(self):
        return f"Camera Point: {self.camera_point}, Target Point: {self.target_point}, Vector Up: {self.vector_up}, Width: {self.hres}, Height: {self.vres}, W: {self.w}, V: {self.v}, U: {self.u}, Target Distance: {self.target_distance}"

    def generate_ray(self, pixel_x, pixel_y):
        # O aspect_ratio garante que a imagem renderizada não fique distorcida, considerando a resolução
        aspect_ratio = self.hres / self.vres
        # Coordenadas normalizadas do pixel em relação ao plano de projeção da câmera
        # canto esquerdo: x = -1 canto direito: x = 1 canto inferior : y = -1 canto superior : y = +1 
        x = (2 * (pixel_x + 0.5) / self.hres - 1) * aspect_ratio   # ajusta a posição do pixel para que esteja centrado no meio do pixel e mantém no intervalo [-1,+1]
        y = 1 - 2 * (pixel_y + 0.5) / self.vres                    # centraliza o pixel e mantém no intervalo [-1,+1]
        direction = (
            self.w.scale(self.target_distance)  # Representa o ponto central do plano de projeção
            + self.v.scale(x)                   # Adiciona um deslocamento horizontal ao ponto no plano de projeção
            + self.u.scale(y)                 # Adciona um deslocamento vertical ao ponto no plano de projeção
        ).normalize()
        return Ray(self.camera_point, direction)

    def ray_casting(self, entities, depth):
        """Ray Casting Method"""

        image = np.zeros((self.hres, self.vres, 3), dtype=np.uint8) # Cria uma imagem preta.


        for i in range(self.vres):
            for j in range(self.hres):
                print(  self.w.scale(depth) +
                        self.v.scale(2 * 0.5 * (j / self.vres - 0.5)) +
                        self.u.scale(2 * 0.5 * (i / self.hres - 0.5)))

                image[i,j]= (251,198,207)


        cv.imshow("image", image)
        cv.waitKey(0)
        cv.destroyAllWindows("i")