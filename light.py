from point import Point



class Light:
    def __init__(self, position: Point, intensity: float):
        self.position = position,
        self.intensity = intensity


    def __str__(self):
        return f"Light: {self.position}  intensidade: {self.intensity}"


