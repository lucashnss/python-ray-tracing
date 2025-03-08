import numpy as np
import cv2 as cv
from camera import Camera
from sphere import Sphere
from mesh import Mesh
from plane import Plane
from phong import phong
from point import Point

class Renderer:
    """
        Classe que representa o renderizador.
        Argumentos:
        camera: câmera
        objects: objetos a serem renderizados
    """
    def __init__(self, camera: Camera, objects: Sphere | Plane | Mesh):
        self.camera = camera
        self.objects = objects
        self.hres = camera.hres
        self.vres = camera.vres
        self.image = np.zeros((self.vres,self.hres,3), dtype=np.uint8)

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
        cv.destroyAllWindows()

    def trace_ray(self, ray):
        # Inicia a cor como preto, assumindo que, inicialmente, o raio não acerta nenhum objeto
        closest_t = float('inf')        # Qualquer distância válida será menor que infinito
        closest_color = np.array([0,0,0])
        # Para cada objeto vamos verificar se o raio intersecta este objeto
        for obj in self.objects:
            light_points_arr = [Point(0, 10, -5), Point(-5, 5, 0), Point(5, 5, 0)] # Fontes de luz

            # Parâmetros de Phong
            ambiental_color_light = np.array([50,50,50])
            Il = [np.array([255, 255, 255]), np.array([255, 255, 200]), np.array([200, 200, 255])]

            R_arr = [] # Inicilializando vetores de reflexão
            light_vectors_arr = [] # Inicializando array de vetores para luz

            #  Se o objeto for uma esfera
            if obj.type == "Sphere":
                t = obj.intersect(ray)

                if t and t < closest_t:
                    closest_t = t
                    # Cálculo do vetor normal do ponto 
                    intersection_point = ray.origin + ray.direction * t
                    normal_vector = (intersection_point - obj.center).normalize()

                    # Definindo e normalizando os vetores dos arrays:
                    for i in range(len(light_points_arr)):
                        light_vector = (light_points_arr[i] - intersection_point).normalize()
                        light_vectors_arr.append(light_vector)
                        reflected_vector = (2 * normal_vector.dot_product(light_vector) * normal_vector - light_vector).normalize()
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
                        ks=obj.k_specular,
                        R=R_arr,
                        V=(ray.origin - intersection_point).normalize(),
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
                    # Verificação se a normal aponta para a direção certa
                    cos = normal_vector.dot_product(ray.direction)
                    if cos < 0:
                        normal_vector = normal_vector * -1

                    # Definindo e normalizando os vetores dos arrays:
                    for i in range(len(light_points_arr)):
                        light_vector = (light_points_arr[i] - intersection_point).normalize()
                        light_vectors_arr.append(light_vector)
                        reflected_vector = (2 * normal_vector.dot_product(light_vector) * normal_vector - light_vector).normalize()
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
                        ks=obj.k_specular,
                        R=R_arr,
                        V=(ray.origin - intersection_point).normalize(),
                        n=obj.n
                    )
                    # Atualizando a cor mais próxima
                    closest_color = final_color
            # Se o objeto for uma malha
            elif obj.type == "Mesh":
                t, normal_vector = obj.intersect(ray)

                if t and t < closest_t:
                    closest_t = t
                    # Cálculo do vetor normal do ponto 
                    intersection_point = ray.origin + ray.direction * t
                    # Verificação se a normal aponta para a direção certa
                    cos = normal_vector.dot_product(ray.direction)
                    if cos < 0:
                        normal_vector = normal_vector * -1

                    # Definindo e normalizando os vetores dos arrays:
                    for i in range(len(light_points_arr)):
                        light_vector = (light_points_arr[i] - intersection_point).normalize()
                        light_vectors_arr.append(light_vector)
                        reflected_vector = (2 * normal_vector.dot_product(light_vector) * normal_vector - light_vector).normalize()
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
                        ks=obj.k_specular,
                        R=R_arr,
                        V=(ray.origin - intersection_point).normalize(),
                        n=obj.n
                    )
                    # Atualizando a cor mais próxima
                    closest_color = final_color
                
        return closest_color