from point import Point
from vector import Vector

class Ray:
    """
        Classe representando um raio de luz.
    Argumentos:
        origin (Point): ponto de origem do raio
        direction (Vector): vetor direção do raio
    """

    def __init__(self, origin: Point, direction: Vector):
        """Initialize the Ray"""
        self.origin = origin
        self.direction = direction.normalize()
