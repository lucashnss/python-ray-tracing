from point import Point
from vector import Vector

class Ray:
    """Class Representing a Ray in 3D Space
    Args:
        origin, direction
    """

    def __init__(self, origin: Point, direction: Vector):
        """Initialize the Ray"""
        self.origin = origin
        self.direction = direction.normalize()

