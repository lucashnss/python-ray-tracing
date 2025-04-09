import math
from point import Point

class BezierSurface:
    """
    Representa uma superfície de Bézier em um espaço tridimensional.
    Atributos:
        control_points (list[list[Point]]): Grade de pontos de controle (m x n).
        color (tuple): Cor da superfície.
        k_ambient (float): Coeficiente de reflexão ambiental.
        k_diffuse (float): Coeficiente de reflexão difusa.
        k_specular (float): Coeficiente de reflexão especular.
        k_reflection (float): Coeficiente de reflexão.
        k_refraction (float): Coeficiente de refração.
        refraction_index (float): Índice de refração.
        n (int): Expoente da componente especular.
    """
    def __init__(self, control_points, color, k_ambient, k_diffuse, k_specular, k_reflection, k_refraction,
                 refraction_index, n):
        self.type = "BezierSurface"
        self.control_points = control_points
        self.color = color
        self.k_ambient = k_ambient
        self.k_diffuse = k_diffuse
        self.k_specular = k_specular
        self.k_reflection = k_reflection
        self.k_refraction = k_refraction
        self.IOR = refraction_index
        self.n = n
        self.m = len(control_points) - 1
        self.np = len(control_points[0]) - 1

    def __str__(self):
        return f"BezierSurface: {self.m + 1}x{self.np + 1} control points"

    def bernstein(self, i, n, t):
        # Calcula o polinômio de Bernstein B_i^n(t)
        return math.comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

    def evaluate(self, u, v):
        # Avalia a superfície de Bézier no ponto (u, v)
        point = Point(0, 0, 0)
        for i in range(self.m + 1):
            for j in range(self.np + 1):
                b_u = self.bernstein(i, self.m, u)
                b_v = self.bernstein(j, self.np, v)
                cp = self.control_points[i][j]
                print(f"b_u: {b_u}, b_v: {b_v}, cp: {cp}")
                point += cp * (b_u * b_v)

        return point

    def intersect(self, ray, samples=10):
        """
        Verifica a interseção do raio com a superfície de Bézier usando amostragem.
        Aproxima a superfície por pontos e verifica o ponto mais próximo ao raio.
        """
        closest_t = None
        min_dist = float('inf')
        for i in range(samples + 1):
            u = i / samples
            for j in range(samples + 1):
                v = j / samples
                surface_point = self.evaluate(u, v)
                to_point = surface_point - ray.origin
                projection_length = to_point.dot_product(ray.direction)
                if projection_length <= 0:
                    continue
                projected = ray.origin + ray.direction * projection_length
                dist = (surface_point - projected).magnitude()
                if dist < 1e-2 and projection_length < min_dist:
                    min_dist = projection_length
                    closest_t = projection_length
        return closest_t
