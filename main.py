import numpy as np
from light import Light
from mesh import Mesh, apply_affine_transformation
from obj_reader import ObjReader
from camera import Camera
from renderer import Renderer
from point import Point
from vector import Vector
from sphere import Sphere
from plane import Plane
from transform import *

def main():
    # Configurações da câmera
    camera = Camera(
        camera_point=Point(0, 0, 5),
        target_point=Point(0, 0, 0),
        vector_up=Vector(0, 1, 0),
        target_distance=1,
        hres=500,
        vres=500
    )

       # Configurações das esferas
    sphere1 = Sphere(
        center=Point(0, -3, -0.5),  # Centro da esfera vermelha
        radius=3,  # Raio da esfera vermelha
        color=np.array([0, 0, 1]),  # Cor da esfera vermelha (vermelho escuro)
        k_ambient=0.1,  # Coeficiente de luz ambiente
        k_diffuse=0.9,  # Coeficiente de luz difusa
        k_specular=0.3,  # Coeficiente de luz especular (baixo ou zero)
        k_reflection=0.0,  # Coeficiente de reflexão
        k_refraction=0.0,  # Coeficiente de refração
        refraction_index=1.0,  # Índice de refração
        n=1  # Expoente especular (baixo)
    )

    sphere2 = Sphere(
        center=Point(5, 0, -1),  # Centro da esfera azul
        radius=2.0,  # Raio da esfera azul
        color=np.array([1, 0, 0]),  # Cor da esfera azul (azul escuro)
        k_ambient=0.1,  # Coeficiente de luz ambiente
        k_diffuse=0.9,  # Coeficiente de luz difusa
        k_specular=0.2,  # Coeficiente de luz especular (baixo ou zero)
        k_reflection=0.0,  # Coeficiente de reflexão
        k_refraction=0.0,  # Coeficiente de refração
        refraction_index=1.0,  # Índice de refração
        n=1  # Expoente especular (baixo)
    )

    sphere3 = Sphere(
        center=Point(-5, 0, -1),  # Centro da esfera verde
        radius=2,  # Raio da esfera verde
        color=np.array([0, 1, 0]),  # Cor da esfera verde (verde escuro)
        k_ambient=0.1,  # Coeficiente de luz ambiente
        k_diffuse=0.9,  # Coeficiente de luz difusa
        k_specular=0.2,  # Coeficiente de luz especular (baixo ou zero)
        k_reflection=0.0,  # Coeficiente de reflexão
        k_refraction=0.0,  # Coeficiente de refração
        refraction_index=1.0,  # Índice de refração
        n=1  # Expoente especular (baixo)
    )

    # Configurações do plano
    plane = Plane(
        point=Point(0, -2, 0),  # Ponto no plano
        normal=Vector(0, 1, 0),  # Vetor normal do plano
        color=np.array([0, 1, 1]),  # Cor do plano (amarelo)
        k_ambient=0.1,  # Coeficiente de luz ambiente
        k_diffuse=0.9,  # Coeficiente de luz difusa
        k_specular=0.1,  # Coeficiente de luz especular (baixo ou zero)
        k_reflection=0.0,  # Coeficiente de reflexão
        k_refraction=0.0,  # Coeficiente de refração
        refraction_index=1.0,  # Índice de refração
        n=1  # Expoente especular (baixo)
    )

    # mesh = Mesh(
    #     n_triangles=3,
    #     n_vertices=8,
    #     vertice_list=[
    #         Point(5, 0, -10),
    #         Point(2, 0, -10),
    #         Point(2, 5, -10),
    #         Point(-5, 0, -10),
    #         Point(-5, 5, -10),
    #         Point(5, 0, -15),
    #         Point(-5, 0, -15),
    #         Point(-5, 5, -15),
    #     ],
    #     triples_list=[
    #         (0, 1, 2),
    #         (2, 3, 4),
    #         (0, 3, 7)
    #     ],
    #     normal_list=[
    #         Vector(0, 0, 1),
    #         Vector(0, 0, 1),
    #         Vector(0, 0, 1),
    #         Vector(0, 0, 1)
    #     ],
    #     vertices_normal_list=[
    #         Vector(0, 0, 1),
    #         Vector(0, 0, 1),
    #         Vector(0, 0, 1)
    #     ],
    #     colors_normalized_list=[
    #         np.array((255, 0, 0)),
    #         np.array([255, 0, 0]),
    #         np.array([255, 0, 0])
    #     ],
    #     color=np.array([255, 0, 0]),
    #     k_ambient=0.3,
    #     k_diffuse=0.7,
    #     k_specular=0.6,
    #     k_reflection=0.2,
    #     k_refraction=0.0,
    #     refraction_index=1.0,
    #     n=30
    # )

    # matrix = translate(-10, -10, 0)
    # triangleTransformed = apply_affine_transformation(triangle, matrix)

    # for vertex in triangleTransformed.vertice_list:
        # print(f"vertex {vertex.array()}")

    objects = [sphere1, sphere2, sphere3, plane]

    # Luzes
    light1 = Light(Point(0, 5, 10), np.array([255, 255, 255]))
    light2 = Light(Point(-5, 5, -10), np.array([255, 255, 255]))
    lights = [light1, light2]
    ambiental_color_light = np.array([50, 50, 50])
    # Cria o renderizador
    renderer = Renderer(camera, objects, lights, ambiental_color_light)
    renderer.render()

if __name__ == "__main__":
    main()
