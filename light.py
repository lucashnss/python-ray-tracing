from point import Point
import numpy as np

class Light:
    """
        Classe que representa uma fonte de luz.
        Argumentos:
        position: posição da fonte de luz
        intensity (conjunto RGB do tipo [[0,255],[0,255], [0,255]]) : intensidade da fonte de luz
    """
    def __init__(self, position: Point, intensity: np.array):
        self.position = position
        self.intensity = intensity