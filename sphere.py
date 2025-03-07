import math
from point import Point

class Sphere:
    def __init__(self, center: "Point", radius, color, k_ambient, k_diffuse, k_specular, k_reflection, k_refraction, 
                refraction_index, n):
        self.type = "Sphere"
        self.center = center
        self.radius = radius
        self.color = color
        self.k_ambient = k_ambient
        self.k_diffuse = k_diffuse
        self.k_specular = k_specular
        self.k_reflection = k_reflection
        self.k_refraction = k_refraction
        self.IOR = refraction_index
        self.n = n

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

        oc = ray.origin - self.center #  (ox - cx, oy - cy, oz - cz)
        a = ray.direction.dot_product(ray.direction) # dx**2 + dy**2 + dz**2
        b = 2 * (oc.dot_product(ray.direction)) # 2 ((ox - cx)*dx + (oy - cy)*dy + (oz - cz)*dz )
        c = oc.dot_product(oc) - self.radius * self.radius # (ox - cx)**2 + (oy - cy)**2 + (oz - cz)**2 - r**2
        discriminant = (b * b) - (4 * a * c) # delta = B**2 - 4AC

        epsilon = 1e-8  # Tolerância para comparação de ponto flutuante
        # Pontos de intersecção
        # Nesse caso não há intersecção entre o raio e a esfera
        if discriminant < 0:
            return None
        # Nesse caso o raio tangencia a esfera
        elif discriminant < epsilon:
            t = -b / (2 * a) # -B/2A
            return t
        else:
            # Se delta > 0 o raio intersecta a esfera em dois ponto
            t1 = (-b + math.sqrt(discriminant)) / (2.0 * a) # (-B + raiz(delta))/2A
            t2 = (-b - math.sqrt(discriminant)) / (2.0 * a) # (-B - raiz(delta))/2A
            # Escolher o menor t positivo para retornar ao Ray Tracing
            if t1 > 0 and t2 > 0:
                return min(t1,t2) # Retorna o menor valor entre t1 e t2
            elif t1 > 0: #
                return t1
            elif t2 > 0:
                return t2
            else:
                return None     # Ambas as intersecções estão atrás da câmera
