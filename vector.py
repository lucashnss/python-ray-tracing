import math
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

    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def normalize(self):
        return Vector(self.x / self.magnitude(), self.y / self.magnitude(), self.z / self.magnitude())

    def cross_product(self, vector):
        return Vector(
            self.y * vector.z - self.z * vector.y,
            self.z * vector.x - self.x * vector.z,
            self.x * vector.y - self.y * vector.x
        )

    def normalize(self):
        return Vector(
            self.x / self.magnitude(),
            self.y / self.magnitude(),
            self.z / self.magnitude()
        )

    def angle(self, vector):
        return math.acos((self * vector) / (self.magnitude() * vector.magnitude()))



