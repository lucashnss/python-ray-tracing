from typing import List
import numpy as np
import cv2 as cv
from camera import Camera
from light import Light
from objects.sphere import Sphere
from objects.mesh import Mesh
from objects.plane import Plane
from vector import Vector
from point import Point
from ray import Ray
import math
import concurrent.futures
from typing import List, Tuple
import time


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
        self.total_pixels = self.hres * self.vres
        self.start_time = time.perf_counter()

    def _render_chunk(self, start_row: int, end_row: int) -> List[Tuple[int, int, np.ndarray]]:
        """Render a chunk of the image rows"""
        chunk_colors = []
      
        for i in range(start_row, end_row):
            if(i%(end_row - ((end_row -start_row)/2)) == 0 or start_row == i):
                print(f"Rendering row {i}/{end_row} time: {time.perf_counter() - self.start_time:.2f} seconds")
            
            for j in range(self.hres):
                self.rendering += 1
               
                ray = self.camera.generate_ray(j, i)
                color = self.trace_ray(ray, self.objects)
                chunk_colors.append((i, j, color))
        end_time = time.perf_counter()
        print(f"Time to render chunk: {end_time - self.start_time:.2f} seconds")
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
           
                future = executor.submit(self._render_chunk, start, end)
                futures.append(future)

            # Track progress
            completed = 0
            total_chunks = len(chunks)
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(futures):
                completed += 1
        
                print(f"{completed}/{total_chunks} chunks completed... {completed / total_chunks * 100:.2f}%")
                # Update image with chunk results
                chunk_colors = future.result()
                for i, j, color in chunk_colors:
                    self.image[i,j] = color
                    

        print('100.00% - Concluído!')
        cv.imwrite("output.png", self.image)
        cv.imshow("Ray Tracing", self.image)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def render_single_thread(self):
        """
        Render the scene using a single thread
        """
        self.start_time = time.perf_counter()
        total_pixels = self.hres * self.vres
        pixels_done = 0

        for i in range(self.vres):
            if i % 10 == 0:  # Print progress every 10 rows
                print(f"Rendering row {i}/{self.vres} time: {time.perf_counter() - self.start_time:.2f} seconds")
            
            for j in range(self.hres):
                ray = self.camera.generate_ray(j, i)
                color = self.trace_ray(ray, self.objects)
                self.image[i,j] = color
                pixels_done += 1
                
                if pixels_done % 1000 == 0:  # Print progress every 1000 pixels
                    print(f"Progress: {pixels_done}/{total_pixels} pixels ({pixels_done/total_pixels*100:.2f}%)")

        end_time = time.perf_counter()
        print(f"Total render time: {end_time - self.start_time:.2f} seconds")
        print('100.00% - Concluído!')
        cv.imwrite("output.png", self.image)
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
    
    def phong(
        self,
        ka: float,
        Ia: np.ndarray,
        Il: List[np.ndarray],
        kd: float,
        Od: np.ndarray,
        N: Vector,
        L: List[Vector],
        ks: float,
        R: List[Vector],
        V: Vector,
        n: int,
        lim_r: int,
        k_r: float,
        camera_vector: Vector,
        objects: Sphere | Plane | Mesh,
        intersection_point: Point,
        current_obj: Sphere | Plane | Mesh,
        k_t: float,
        n_in: float,
        n_out: float,
        reflection: bool = True,
        refraction: bool = True,
        counter_r: int = 0,
    ) -> np.ndarray:
        """
        ka (between 0 and 1): ambient coefficient
        Ia (RGB between 0 and 255): ambient light color
        Il (list of RGBs): light colors
        kd (between 0 and 1): diffuse coefficient
        Od (RGB between 0 and 255): object color
        N (vector): normal vector
        L (list of vectors): light directions
        ks (between 0 and 1): specular coefficient
        R (list of vectors): reflected ray directions
        V (vector): camera direction
        n (integer): specular exponent
        lim_r (integer): max number of reflections
        k_r (between 0 and 1): reflection coefficient
        camera_vector (vector): camera direction
        objects (list of objects): list of objects that can reflect or refract light
        intersection_point (point): intersection point with the object
        current_obj (object): current object
        k_t (between 0 and 1): refraction coefficient
        n_in (float): refraction index in
        n_out (float): refraction index out
        reflection (boolean): reflection enabled
        refraction (boolean): refraction enabled
        counter_r (integer): number of recursive calls

        Returns:
            RGB color of the object
        """
        # Normalize components
        Ia = Ia / 255.0
        Il = np.array(Il) / 255.0

        # Ambient component
        environmental_component = ka * Ia
        diffuse_component = np.zeros(3)
        specular_component = np.zeros(3)
        reflection_component = np.zeros(3)
        refraction_component = np.zeros(3)

        for i in range(len(Il)):
            # Calculate diffuse and specular components
            diffuse_component += kd * Il[i] * max(0, N.dot_product(L[i])) * Od
            specular_component += ks * Il[i] * max(0, (R[i].dot_product(V)) ** n)

        if counter_r <= lim_r:
            # Calculate reflection component
            nextCounter = counter_r + 1
            if reflection and k_r != 0:
                reflected_vector = (2 * N.dot_product(camera_vector) * N - camera_vector).normalize()
                reflected_vector = reflected_vector * -1
                Ir = self.trace_ray(
                    ray=Ray(intersection_point, reflected_vector),
                    objects=objects,
                    counter_r=nextCounter,
                    reflection=True,
                    refraction=True,
                    n_in=n_out,
                    
                )
                Ir = Ir / 255.0
                reflection_component = k_r * Ir

            # Calculate refraction component
            if refraction and k_t != 0:
                snell = n_in / n_out
                cos_theta = N.dot_product(camera_vector)
                cost_theta_t = self.cos_theta_t(n_in, n_out, cos_theta)
                if type(cost_theta_t) != str:
                    refracted_vector = (
                        (1 / snell) * camera_vector - ((cost_theta_t - (1 / snell) * cos_theta) * N)
                    ).normalize()
                    It = self.trace_ray(
                        ray=Ray(intersection_point, refracted_vector),
                        objects=objects,
                        counter_r=nextCounter,
                        n_in=n_out,
                        reflection=True,
                        refraction=True,
                    )
                    It = It / 255.0
                    refraction_component = k_t * It

        final_color = (
            environmental_component + diffuse_component + specular_component
            + reflection_component + refraction_component
        )
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
                        lim_r=3,
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