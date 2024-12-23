import numpy as np
import cv2 as cv
from camera import Camera
from sphere import Sphere
from plane import Plane

class Renderer:
    def __init__(self, camera: Camera, objects: Sphere | Plane, hres:int, vres:int):
        self.camera = camera
        self.objects = objects
        self.hres = hres
        self.vres = vres
        self.image = np.zeros((vres,hres,3), dtype=np.uint8)

    def render(self):
        for i in range(self.vres):
            for j in range(self.hres):
                ray = self.camera.generate_ray(j,i)
                color = self.trace_ray(ray)
                self.image[i,j] = color  # A matriz numpy por padrão é image[índice linha, índice coluna]

        cv.imshow("Ray Tracing", self.image)
        cv.waitKey(0)
        cv.destroyAllWindows("e")

    def trace_ray(self, ray):
        # Inicia a cor como preto, assumindo que, inicialmente, o raio não acerta nenhum objeto
        closest_t = float('inf')        # Qualquer distância válida será menor que infinito
        closest_color = (0,0,0)
        # Para cada objeto vamos verificar se o raio intersecta este objeto
        for obj in self.objects:
            t = obj.intersect(ray)

            if t and t < closest_t:
                closest_t = t
                closest_color = obj.color

        return closest_color
