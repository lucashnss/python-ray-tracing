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

            print(f"{(i/self.vres)*100:.2f}%")
            for j in range(self.hres):
                ray = self.camera.generate_ray(j,i)
                color = self.trace_ray(ray)
                self.image[i,j] = color  # A matriz numpy por padrão é image[índice linha, índice coluna]

        print('100.00% - Concluído!')
        cv.imshow("Ray Tracing", self.image)
        cv.waitKey(0)
        cv.destroyAllWindows("e")

    def phong(self, ka, Ia, Il, kd, Od, N, L, ks, R, V, n):
        """
            ka (entre 0 e 1): coeficiente ambiental
            Ia (conjunto RGB do tipo [[0,255],[0,255], [0,255]]): cor da luz ambiental
            Il (array de RGBs do tipo [[0,255], [0,255], [0,255],  ...]) = array com as luzes do ambiente
            kd (entre 0 e 1): coeficiente de difusão do objeto
            Od (conjunto RGB do tipo [[0,255],[0,255], [0,255]]): conjunto RGB que representa a cor do objeto
            N (vetor): vetor normal ao ponto de interseção do objeto com a câmera
            L (array de vetores): vetores que representam as direções das luzes
            ks (entre 0 e 1): coeficiente especular do objeto
            R (array de vetores): vetores que representam as direções dos raios refletidos
            V (vetor): vetor que representa a direção da câmera
            n (inteiro): expoente da componente especular do objeto
        Retorna:
                Um vetor RGB que representa a cor final do objeto

        """
        # Normalização das componentes
        Ia = np.array(Ia)/255.0
        Il = np.array(Il)/255.0
        Od = np.array(Od)/255.0

        # Componente Ambiental
        environmental_component = ka * Ia

        diffuse_component = np.zeros(3)
        specular_component = np.zeros(3)

        for i in range(len(Il)):
            # Cálculo da componente difusa e da componente especular
            diffuse_component += kd * Il[i] * np.maximum(0, np.dot(N, L[i])) * Od
            specular_component += ks * Il[i] * np.maximum(0, np.dot(R[i], V)**n)

        final_color = environmental_component + diffuse_component + specular_component
        final_color = np.clip(final_color, 0, 1) * 255

        return final_color

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
