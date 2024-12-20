from vector import Vector

class Point:

    """
    Representa um ponto em um espaço tridimensional.

    Atributos:
        x (float): Componente do ponto no eixo X.
        y (float): Componente do ponto no eixo Y.
        z (float): Componente do ponto no eixo Z.
    """
    def __init__(self, x: float, y: float, z:float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y, self.z + point.z)

    def __sub__(self, point):
        return Vector(self.x - point.x, self.y - point.y, self.z - point.z)

    def dot_product(self, point1):
        return self.x * point1.x + self.y * point1.y + self.z * point1.z

    def distance(self, point):
        return ((self.x - point.x) ** 2 + (self.y - point.y) ** 2 + (self.z - point.z) ** 2) ** 0.5
