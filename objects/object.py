from abc import ABC, abstractmethod
from typing import Optional
from ray import Ray  # Correção aqui
from point import Point
from vector import Vector
import numpy as np

class Object(ABC):
    """
    Classe abstrata que representa um objeto.
    Argumentos:
    color: cor do objeto
    k_ambient: coeficiente de reflexão ambiente
    k_diffuse: coeficiente de reflexão difusa
    k_specular: coeficiente de reflexão especular
    k_reflection: coeficiente de reflexão
    k_refraction: coeficiente de refração
    refraction_index: índice de refração
    n: expoente de Phong
    """
    def __init__(self, color: np.ndarray, k_ambient: float, k_diffuse: float, k_specular: float, 
                 k_reflection: float, k_refraction: float, refraction_index: float, n:int):
        self.type = "Object"
        self.color = color
        self.k_ambient = k_ambient
        self.k_diffuse = k_diffuse
        self.k_specular = k_specular
        self.k_reflection = k_reflection
        self.k_refraction = k_refraction
        self.IOR = refraction_index
        self.n = n
    
    @abstractmethod
    def intersect(self, ray: Ray) -> Optional[float]:
        """Método abstrado que calcula a interseção entre um raio e o objeto."""
        pass

    @abstractmethod
    def normal(self, point: Point) -> Vector:
        """Método abstrado que calcula a normal em um ponto do objeto."""
        pass