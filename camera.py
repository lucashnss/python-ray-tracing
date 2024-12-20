from point import Point
from vector import Vector

class Camera:
    """Class Representing a Camera in 3D Space
        w is the vector that always points to the center of the screen
        v is the vector that's always points to the right and it's ortogonal to w and up
        u is the vector that's always points up and it's ortogonal to w and v
    Args:
        camera_point: Point, target_point: Point, vector_up: Vector, width: int, height: int
    """

    def __init__(self, camera_point: "Point", target_point: "Point", vector_up: "Vector", width: int, height: int):
        self.camera_point = camera_point
        self.target_point = target_point # Ponto para onde a câmera está apontando.
        self.vector_up = vector_up # Vetor que aponta para cima.
        self.width = width # Largura da imagem.
        self.height = height    # Altura da imagem.

        self.w = self.target_point - camera_point # Vetor que aponta para o ponto para onde a câmera está apontando.
        self.v = self.vector_up.cross_product(self.w) # Vetor que aponta para a direita.

        self.w = self.w.normalize() # Normalização do vetor que está apontando para a câmera.
        self.v = self.v.normalize() # Normalização do vetor que está apontando para a direita.

        self.u = self.w.cross_product(self.v) # Vetor que aponta para cima.
        self.u = self.u.normalize() # Normalização do vetor que está apontando para cima.

        self.target_distance = self.camera_point.distance(self.target_point) # Distância entre a câmera e o ponto para onde ela está apontando.

    def __str__(self):
        return f"Camera Point: {self.camera_point}, Target Point: {self.target_point}, Vector Up: {self.vector_up}, Width: {self.width}, Height: {self.height}"
