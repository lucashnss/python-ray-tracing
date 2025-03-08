import math
import numpy as np

class Vector:
    """
    Representa um vetor em um espaço tridimensional.

    Atributos:
        x (float): Componente do vetor na direção X.
        y (float): Componente do vetor na direção Y.
        z (float): Componente do vetor na direção Z.
    """
    def __init__(self, x: float, y: float, z:float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y, self.z + vector.z)

    def __sub__(self, vector):
        return Vector(self.x - vector.x, self.y - vector.y, self.z - vector.z)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar):
        """Permite a multiplicação por escalar à esquerda (escalar * vetor)."""
        return self.__mul__(scalar)

    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector(0, 0, 0)
        else:
            return Vector(self.x / mag, self.y / mag, self.z / mag)

    def cross_product(self, vector):
        return Vector(
            self.y * vector.z - self.z * vector.y,
            self.z * vector.x - self.x * vector.z,
            self.x * vector.y - self.y * vector.x
        )

    def dot_product(self, vector):
        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def scale(self, t):
        return Vector(self.x * t, self.y * t, self.z * t)

    def angle(self, vector):
        # Calcula o ângulo entre dois vetores usando o produto escalar
        dot_product = self.dot_product(vector)
        magnitudes = self.magnitude() * vector.magnitude()
        return math.acos(dot_product / magnitudes)

    def array(self):
        return np.array([self.x, self.y, self.z])