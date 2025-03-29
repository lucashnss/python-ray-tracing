from typing import List
import numpy as np
import cv2 as cv
from camera import Camera
from light import Light
from objects.sphere import Sphere
from objects.mesh import Mesh
from objects.plane import Plane
from ray import Ray
import math
import concurrent.futures
from typing import List, Tuple

class Renderer:
    """
        Classe que representa o renderizador.
        Argumentos:
        camera: câmera
        objects: objetos a serem renderizados
    """
    def __init__(self, camera: Camera, objects: Sphere | Plane | Mesh, lights: List[Light], 
                ambiental_color_light=np.array([255, 255, 255])) -> None:
        self.camera = camera
        self.objects = objects
        self.hres = camera.hres
        self.vres = camera.vres
        self.image = np.zeros((self.vres,self.hres,3), dtype=np.uint8)
        self.lights = lights
        self.ambiental_color_light = ambiental_color_light
        self.rendering = 0

    def _render_chunk(self, start_row: int, end_row: int) -> List[Tuple[int, int, np.ndarray]]:
        """Render a chunk of the image rows"""
        chunk_colors = []
        for i in range(start_row, end_row):
            self.rendering += 1
            print(f"Rendering rows: {self.rendering}/{self.vres} ({(self.rendering / self.vres) * 100:.2f}%)")
            for j in range(self.hres):
               
                ray = self.camera.generate_ray(j, i)
                color = self.trace_ray(ray, self.objects)
                chunk_colors.append((i, j, color))
        return chunk_colors

    def render(self, num_threads=8):
        """
        Render the scene using multiple threads
        Args:
            num_threads: Number of threads to use for rendering
        """
        # Calculate chunk size for each thread
        chunk_size = max(1, self.vres // num_threads)
        chunks = []
        
        # Create chunks of rows to process
        for i in range(0, self.vres, chunk_size):
            end = min(i + chunk_size, self.vres)
            chunks.append((i, end))

        # Process chunks in parallel using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for start, end in chunks:
                print(f"Rendering rows {start} to {end}...")
                future = executor.submit(self._render_chunk, start, end)
                futures.append(future)

            # Track progress
            completed = 0
            total_chunks = len(chunks)
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(futures):
                completed += 1
        
                
                # Update image with chunk results
                chunk_colors = future.result()
                for i, j, color in chunk_colors:
                    self.image[i,j] = color
                    

        print('100.00% - Concluído!')
        cv.imshow("Ray Tracing", self.image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def cos_theta_t(self, n_in, n_out, cos_theta_in):
        # Calcular o seno do ângulo de incidência
        sin_theta_in = np.sqrt(1 - cos_theta_in**2)

        # Aplicar a lei de Snell para calcular o seno do ângulo de refração
        sin_theta_t = (n_in/n_out) * sin_theta_in

        # Verificar se o ângulo de refração é maior que 1, o que indica que ocorre reflexão total
        if sin_theta_t > 1.000001:
            return "Reflexão total interna"
        
        # Calcular o cosseno do ângulo de refração
        cos_theta_t = np.sqrt(1 - sin_theta_t**2)

        return cos_theta_t
    
    def phong(self, ka, Ia, Il, kd, Od, N, L, ks, R, V, n, lim_r, k_r, camera_vector, objects, intersection_point, 
              current_obj, k_t, n_in, n_out, reflection=True, refraction=True, counter_r=0):
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
            lim_r (inteiro): limite de reflexões
            k_r (entre 0 e 1): coeficiente de reflexão do objeto
            camera_vector (vetor): vetor que vem do observador para calcular a reflexão
            objects (lista de objetos): lista de objetos que podem refletir ou refratar a luz
            intersection_point (ponto): ponto de interseção do objeto com a câmera
            current_obj (objeto): objeto atual resultado da intersecção
            k_t (entre 0 e 1): coeficiente de refração do objeto
            n_in (inteiro >=0): índice de refração na entrada da superfície
            n_out (inteiro >= 1): índice de refração na saída da superfície
            reflection (boolean): indica se o objeto está refletindo a luz
            refraction (boolean): indica se o objeto está refratando a luz
            counter_r (inteiro): incrementa em um a cada chamada recursiva de phong
        Retorna:
                Um vetor RGB que representa a cor final do objeto

        """
        # Normalização das componentes
        Ia = Ia/255.0
        Il = np.array(Il)/255.0

        # Componente Ambiental
        environmental_component = ka * Ia
        diffuse_component = np.zeros(3)
        specular_component = np.zeros(3)
        reflection_component = np.zeros(3)
        refraction_component = np.zeros(3)

        for i in range(len(Il)):
                # Cálculo da componente difusa e da componente especular
                diffuse_component += kd * Il[i] * max(0, N.dot_product(L[i])) * Od
                specular_component += ks * Il[i] * max(0, (R[i].dot_product(V))**n)

        if counter_r <= lim_r:
            # Cálculo da componente de reflexão
            if reflection and (k_r != 0):
                reflected_vector = (2 * N.dot_product(camera_vector) * N - camera_vector).normalize()
                reflected_vector = reflected_vector * -1
                Ir = self.trace_ray(ray=Ray(intersection_point, reflected_vector), objects=objects,counter_r=counter_r+1, 
                                    reflection=True, refraction=False)
                Ir = Ir/255.0
                reflection_component = k_r * Ir
            if refraction and (k_t != 0):
                snell = n_in / n_out
                cos_theta = N.dot_product(camera_vector)
                cost_theta_t = self.cos_theta_t(n_in, n_out, cos_theta)
                if type(cost_theta_t) != str:
                    refracted_vector = ((1/snell) * camera_vector - ((cost_theta_t - (1/snell) * cos_theta) * N)).normalize()
                    It = self.trace_ray(ray=Ray(intersection_point, refracted_vector), objects=objects, counter_r=counter_r+1, 
                                        n_in=n_out, reflection=False, refraction=True)
                    It = It/255.0
                    refraction_component = k_t * It

        final_color = environmental_component + diffuse_component + specular_component + reflection_component + refraction_component
        final_color = np.clip(final_color, 0, 1) * 255

        return final_color

    def trace_ray(self, ray, objects, counter_r=0,  n_in=1, reflection=True, refraction=True):
        # Inicia a cor como preto, assumindo que, inicialmente, o raio não acerta nenhum objeto
        closest_t = float('inf')        # Qualquer distância válida será menor que infinito
        closest_color = np.array([0,0,0])

        # Para cada objeto vamos verificar se o raio intersecta este objeto
        for obj in self.objects:
            #  Se o objeto for uma esfera
            t = obj.intersect(ray)
            
            if n_in == 1:
                n_out = obj.IOR
            else:
                n_out = 1

            if t:
                if t >= 0.01 and t < closest_t:
                    closest_t = t   

                # Cálculo do vetor normal do ponto
                    intersection_point = ray.origin + ray.direction * t
                    if(obj.type == "Mesh"):
                        normal_vector = obj.closest_normal
                    else:
                        normal_vector = (obj.normal(intersection_point)).normalize()

                    # Verificação se a normal aponta para a direção certa
                    cos = normal_vector.dot_product(ray.direction)
                    if cos > 0:
                        normal_vector = normal_vector * -1

                    # Parâmetros de Phong
                    Il = [] # Inicizalizando array da intensidade das luzes
                    R_arr = [] # Inicilializando vetores de reflexão
                    light_vectors_arr = [] # Inicializando array de vetores para luz

                    # Definindo e normalizando os vetores dos arrays:
                    for light in self.lights:
                        light_vector = (light.position - intersection_point).normalize()
                        light_vectors_arr.append(light_vector)
                        reflected_vector = (2 * normal_vector * normal_vector.dot_product(light_vector) - light_vector).normalize()
                        R_arr.append(reflected_vector)

                        # Checagem de sombra
                        shadowed = False
                        shadow_Ray = Ray(intersection_point + normal_vector * 0.0001, light_vector)
                        for shadow_obj in self.objects:
                            shadow_t = shadow_obj.intersect(shadow_Ray)
                            if shadow_t and (light.position - intersection_point).magnitude() > shadow_t:
                                shadowed = True
                                break
                        
                        if shadowed:
                            Il.append(np.array([0,0,0]))
                        else:
                            Il.append(light.intensity)

                    # Cálculo da cor do pixel
                    final_color = self.phong(
                        ka=obj.k_ambient,
                        Ia=self.ambiental_color_light,
                        Il=Il,
                        kd=obj.k_diffuse,
                        Od=obj.color,
                        N=normal_vector,
                        L=light_vectors_arr,
                        ks=obj.k_specular,
                        R=R_arr,
                        V=(ray.origin - intersection_point).normalize(),
                        n=obj.n,
                        lim_r=0,
                        k_r=obj.k_reflection,
                        camera_vector=ray.direction.normalize(),
                        objects=objects,
                        intersection_point=intersection_point,
                        current_obj=obj,
                        counter_r=counter_r,
                        k_t=obj.k_refraction,
                        reflection=reflection,
                        refraction=refraction,
                        n_in=n_in,
                        n_out=n_out
                    )
               

                    closest_color = final_color
        return closest_color