class Plane:
    """Plane Class"""

    def __init__(self, point, normal, color):
        self.point = point # Ponto no plano
        self.normal = normal # Vetor normal do plano
        self.color = color # Cor do plano

    def __str__(self):
        return f"Plane: {self.point} {self.normal} {self.color}"

    def intersect(self, ray):
        """Intersect Method"""
        direction = ray.origin - self.point
        dot_result = self.normal.dot(ray.direction)



    def __normal__(self, point):
        """Normal Method"""
        return self.normal

