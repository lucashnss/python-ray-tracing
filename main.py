import numpy as np
from light import Light
from objects.mesh import Mesh, apply_affine_transformation
from obj_reader import ObjReader
from camera import Camera
from renderer import Renderer
from point import Point
from vector import Vector
from objects.sphere import Sphere
from objects.plane import Plane
from transform import affine_transform, translate


def main():
    # Configurações da câmera
    camera = Camera(
        camera_point=Point(0,0,5),
        target_point=Point(0,0,3),
        vector_up=Vector(0, 1, 0),
        target_distance=1,
        hres=500,
        vres=500,
    )

    # camera = Camera(
    #     camera_point=Point(6, 1, 2),
    #     target_point=Point(
    #         6, 1, 0),
    #     vector_up=Vector(0, 1, 0),
    #     target_distance=1,
    #     hres=500,
    #     vres=500,
    #)

    # Transformações afins

    # Configurações das esferas
    sphere1 = Sphere(
        center=Point(0, 0,  -2),
        radius=2,
        color=np.array([0, 0, 1]),  # Cor da esfera vermelha
        k_ambient=0,
        k_diffuse=0.1,
        k_specular=0.3,
        k_reflection=0.1,
        k_refraction=1.0,
        refraction_index=1.3,
        n=500,
    )


    sphere2 = Sphere(
        center=Point(4, 0, 0),
        radius=2.0,
        color=np.array([1, 0, 0]),  # Cor da esfera azul
        k_ambient=0.3,
        k_diffuse=0,
        k_specular=0.5,
        k_reflection=1,
        k_refraction=0,
        refraction_index=1.52,
        n=500,
    )

    sphere3 = Sphere(
        center=Point(-4, 0,  3),
        radius=2,
        color=np.array([0, 1, 0]),  # Cor da esfera verde
        k_ambient=0.3,
        k_diffuse=0.5,
        k_specular=0.5,
        k_reflection=0.0,
        k_refraction=0.0,
        refraction_index=1,
        n=100,
    )




    # Configurações do plano
    plane = Plane(
        point=Point(0, -2, 0),
        normal=Point(0, -2, 0) - Point(0,1,0),
        color=np.array([0, 1, 1]),  # Cor do plano (amarelo)
        k_ambient=1,
        k_diffuse=1,
        k_specular=1,
        k_reflection=0.0,
        k_refraction=0.0,
        refraction_index=1,
        n=500,
    )

    plane2 = Plane(
        point=Point(0, 0, -10),
        normal=Point(0, 0, -10) - Point(0,0,1),
        color=np.array([0, 1, 0]),  # Cor do plano (amarelo)
        k_ambient=1,
        k_diffuse=1,
        k_specular=1,
        k_reflection=0,
        k_refraction=0.0,
        refraction_index=1,
        n=500,
    )
    plane3 = Plane(
        point=Point(-8, 0, 0),
        normal=Point(-8, 0, 0) - Point(1,0,0),
        color=np.array([1, 1, 0]),  # Cor do plano (amarelo)
        k_ambient=1,
        k_diffuse=1,
        k_specular=1,
        k_reflection=0.0,
        k_refraction=0.0,
        refraction_index=1,
        n=500,
    )

    mesh = Mesh(
        n_triangles=3,
        n_vertices=8,
        vertice_list=[
            Point(5, 0, -10),
            Point(2, 0, -10),
            Point(2, 5, -10),
            Point(-5, 0, -10),
            Point(-5, 5, -10),
            Point(5, 0, -15),
            Point(-5, 0, -15),
            Point(-5, 5, -15),
        ],
        triples_list=[(0, 1, 2), (2, 3, 4), (0, 3, 7)],
        normal_list=[
            Vector(0, 0, 1),
            Vector(0, 0, 1),
            Vector(0, 0, 1),
        ],
        vertices_normal_list=[Vector(0, 0, 1), Vector(0, 0, 1), Vector(0, 0, 1)],
        colors_normalized_list=[
            np.array((1, 0, 0)),
            np.array([0, 1, 0]),
            np.array([0, 0, 1]),
        ],
        color=np.array([1, 0, 0]),
        k_ambient=0.3,
        k_diffuse=0.7,
        k_specular=0.6,
        k_reflection=0.2,
        k_refraction=0.0,
        refraction_index=1,
        n=30,
    )

    matrix = translate(-10, -10, 0)
    meshTransformerd = apply_affine_transformation(mesh, matrix)


    reader = ObjReader("inputs/cubo.obj")
    # # reader = ObjReader("inputs/macaco.obj")
    reader.read_file()

    mesh = reader.create_mesh()
    objects = [plane,plane2, plane3, sphere2, sphere1, sphere3,  ]

    # Luzes
   
    light2 = Light(Point(10, 50, 50), np.array([255, 255, 255]))
  
    lights = [light2]
    ambiental_color_light = np.array([50, 50, 50])
    # Cria o renderizador
    renderer = Renderer(camera, objects, lights, ambiental_color_light)
    renderer.render()


if __name__ == "__main__":
    main()
