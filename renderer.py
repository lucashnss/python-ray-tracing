import numpy as np
import cv2 as cv
from camera import Camera
from sphere import Sphere
from plane import Plane
from phong import phong

def normalize(vector):
    return vector / np.linalg.norm(vector)

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

    def trace_ray(self, ray):
        # Inicia a cor como preto, assumindo que, inicialmente, o raio não acerta nenhum objeto
        closest_t = float('inf')        # Qualquer distância válida será menor que infinito
        closest_color = (0,0,0)
        # Para cada objeto vamos verificar se o raio intersecta este objeto
        for obj in self.objects:
            light_points_arr = np.array([np.array([0,0,0])]) # Fontes de luz

            # Parâmetros de Phong
            ambiental_color_light = np.array([255,255,255])
            Il = [np.array([255,255,255])]

            R_arr = [] # Inicilializando vetores de reflexão
            light_vectors_arr = [] # Inicializando array de vetores para luz

            #  Se o objeto for uma esfera
            if obj.type == "Sphere":
                t = obj.intersect(ray)

                if t and t < closest_t:
                    closest_t = t
                    # Cálculo do vetor normal do ponto 
                    intersection_point = ray.origin + ray.direction * t
                    normal_vector = normalize(intersection_point - obj.center)

                    # Definindo e normalizando os vetores dos arrays:
                    for i in range(len(light_points_arr)):
                        light_vector = normalize(light_points_arr[i] - intersection_point)
                        light_vectors_arr.append(light_vector)
                        reflected_vector = normalize(2 * np.dot(normal_vector, light_vector) * normal_vector - light_vector)
                        R_arr.append(reflected_vector)

                    # Cálculo da cor do pixel
                    final_color = phong(
                        ka=obj.k_ambient,
                        Ia=ambiental_color_light,
                        Il=Il,
                        kd=obj.k_diffuse,
                        Od=obj.color,
                        N=normal_vector,
                        L=light_vectors_arr,
                        R=R_arr,
                        V=normalize(ray.origin - intersection_point),
                        n=obj.n
                    )
                    # Atualizando a cor mais próxima
                    closest_color = final_color
            # Se o objeto for um plano
            elif obj.type == "Plane":
                t = obj.intersect(ray)

                if t and t < closest_t:
                    closest_t = t
                    # Cálculo do vetor normal do ponto 
                    intersection_point = ray.origin + ray.direction * t
                    normal_vector = obj.normal

                    # Definindo e normalizando os vetores dos arrays:
                    for i in range(len(light_points_arr)):
                        light_vector = normalize(light_points_arr[i] - intersection_point)
                        light_vectors_arr.append(light_vector)
                        reflected_vector = normalize(2 * np.dot(normal_vector, light_vector) * normal_vector - light_vector)
                        R_arr.append(reflected_vector)

                    # Cálculo da cor do pixel
                    final_color = phong(
                        ka=obj.k_ambient,
                        Ia=ambiental_color_light,
                        Il=Il,
                        kd=obj.k_diffuse,
                        Od=obj.color,
                        N=normal_vector,
                        L=light_vectors_arr,
                        R=R_arr,
                        V=normalize(ray.origin - intersection_point),
                        n=obj.n
                    )
                    # Atualizando a cor mais próxima
                    closest_color = final_color
            # Se o objeto for uma malha
            elif obj.type == "Mesh":
                pass

        

        return closest_color