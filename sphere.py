import math
from point import Point

class Sphere:
    def __init__(self, center: "Point", radius, color):
        self.center = center
        self.radius = radius
        self.color = color
    
    def __str__(self):
        return f"Sphere: {self.center} {self.radius} {self.color}"
    
    def intersect(self, ray):
        """Intersect Method"""
        # Intersecção de raios com esferas é dado por
        # equação de esfera: (x - cx)** 2 + (y - cy)**2 + (z - cz)**2 = r**2
        # equação paramétrica do raio: R(t) = O + t * D 
        # Substituindo a equação do raio na esfera:
        # (ox + t*dx - cx)** 2 + (oy + t*dy - cy)**2 + (oz + t*dz - cz)**2 = r**2
        # Equação quadrática:
        # A*t**2 + B*t + C = 0
        # A = dx**2 + dy**2 + dz**2
        # B = 2 ((ox - cx)*dx + (oy - cy)*dy + (oz - cz)*dz )
        # C = (ox - cx)**2 + (oy - cy)**2 + (oz - cz)**2 - r**2
        oc = ray.origin - self.center
        a = ray.direction.dot_product(ray.direction)
        b = 2 * (oc.dot_product(ray.direction))
        c = oc.dot_product(oc) - self.radius * self.radius
        discriminant = (b * b) - (4 * a * c)

        epsilon = 1e-6  # Tolerância para comparação de ponto flutuante
        # Pontos de intersecção
        # Nesse caso não há intersecção entre o raio e a esfera
        if discriminant < 0:
            return None
        # Nesse caso o raio tangencia a esfera 
        elif discriminant < epsilon:
            t = -b / (2 * a)
            return t
        else:
            # Se delta > 0 o raio intersecta a esfera em dois ponto
            t1 = (-b + math.sqrt(discriminant)) / (2.0 * a)
            t2 = (-b - math.sqrt(discriminant)) / (2.0 * a)
            return t1, t2 


