class Plane:
    """Plane Class"""

    def __init__(self, point, normal, color):
        self.point = point # Ponto no plano
        self.normal = normal # Vetor normal do plano
        self.color = color # Cor do plano

    def __str__(self):
        return f"Plane: {self.point} {self.normal} {self.color}"

    def __normal__(self, point):
        """Normal Method"""
        return self.normal

    def intersect(self, ray):
        """Intersect Method"""
        # Intersecção de raio com plano é dado por
        # t = N * (Po - O)/ N * D
        # equação paramétrica do raio: R(t) = O + t * D
        # equação do plano: N * (P - Po) = 0 ->  N * P = N * Po
        # Desenvolvimento
        # N * (O + t * D) = N * Po
        # N * O + N * t * D = N * Po
        # t = N * Po - N * O/  N * D
        # t = N * (Po - O)/ (N * D)
        denominator = self.normal.dot_product(ray.direction) # N * D

        # se N * D = 0 então o raio e o plano são paralelos.
        # 1e - 6 é um arredondamento por conta da imprecisão dos cálculos com número flutuante (1e-6 = 10-6)
        epsilon = 1e-6  # Tolerância para comparação de ponto flutuante
        if abs(denominator) < epsilon:
            return None

        direction = self.point - ray.origin  # (Po - O)
        t = self.normal.dot_product(direction)/denominator # N * (Po - O) / N * D
        # Caso em que a intersecção ocorre atrás da câmera
        if t < 0:
            return None

        # Ponto de intersecção
        return t if t > 0 else None # Apenas intersecções na frente da câmera
