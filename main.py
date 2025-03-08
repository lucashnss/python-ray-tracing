import numpy as np
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
        center=Point(-2.5, 0, -1),
        radius=2,
        color=np.array([255, 0, 0]),
        k_ambient=0.2,
        k_diffuse=0.7,
        k_specular=0.3,
        k_reflection=0.3,
        k_refraction=0.0,
        refraction_index=1.0,
        n=30
    )

    sphere2 = Sphere(
        center=Point(2, 0, -1),
        radius=2.5,
        color=np.array([0, 0, 255]),
        k_ambient=0.2,
        k_diffuse=0.7,
        k_specular=0.3,
        k_reflection=0.3,
        k_refraction=0.0,
        refraction_index=1.0,
        n=30
    )

    # Configurações do plano
    plane = Plane(
        point=Point(0, -1, 0),
        normal=Vector(0, 1, 0),
        color=np.array([0, 255, 0]),
        k_ambient=0.2,
        k_diffuse=0.8,
        k_specular=0.1,
        k_reflection=0.2,
        k_refraction=0.0,
        refraction_index=1.0,
        n=20
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

    objects = [sphere1, sphere2, plane] 
    renderer = Renderer(camera, objects)
    renderer.render()

if __name__ == "__main__":
    main()