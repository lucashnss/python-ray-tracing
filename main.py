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
        camera_point=Point(0, 0, 5),
        target_point=Point(0, 0, 0),
        vector_up=Vector(0, 1, 0),
        target_distance=1,
        hres=500,
        vres=500,
    )

    # Transformações afins

    # Configurações das esferas
    sphere1 = Sphere(
        center=Point(0, 0, -1),
        radius=1,
        color=np.array([0, 0, 1]),  # Cor da esfera vermelha
        k_ambient=0.3,
        k_diffuse=0.7,
        k_specular=0.3,
        k_reflection=0.5,
        k_refraction=0.5,
        refraction_index=1.52,
        n=500,
    )

    point = Point(0, -3, -0.5)
    point_transformed = affine_transform([point.x, point.y, point.z], 'translate', -2, 4, 0)

    sphere1_transformed = Sphere(
        center=Point(point_transformed[0], point_transformed[1], point_transformed[2]),
        radius=3,
        color=np.array([0, 1, 0]),
        k_ambient=0.3,
        k_diffuse=0.7,
        k_specular=0.3,
        k_reflection=0.7,
        k_refraction=0.7,
        refraction_index=1.52,
        n=500,
    )

    sphere2 = Sphere(
        center=Point(4, 0, -2),
        radius=2.0,
        color=np.array([1, 0, 0]),  # Cor da esfera azul
        k_ambient=0.3,
        k_diffuse=0.5,
        k_specular=0.5,
        k_reflection=0.8,
        k_refraction=0.2,
        refraction_index=1.52,
        n=500,
    )

    sphere3 = Sphere(
        center=Point(-4, 0, -2),
        radius=2,
        color=np.array([0, 1, 0]),  # Cor da esfera verde
        k_ambient=0.3,
        k_diffuse=0.5,
        k_specular=0.5,
        k_reflection=0.0,
        k_refraction=0.0,
        refraction_index=1.52,
        n=500,
    )

    sphere4 = Sphere(
        center=Point(3, 2, 0),
        radius=1,
        color=np.array([1, 1, 0]),  # Cor da esfera cianeza
        k_ambient=0.3,
        k_diffuse=0.6,
        k_specular=0.8,
        k_reflection=0.5,
        k_refraction=0.0,
        refraction_index=1.52,
        n=500,
    )

    sphere5 = Sphere(
        center=Point(-3, 2, 0),
        radius=1,
        color=np.array([1, 1, 1]),  # Cor da esfera branca (branco)
        k_ambient=0.3,
        k_diffuse=0.3,
        k_specular=0.,
        k_reflection=1,
        k_refraction=1,
        refraction_index=1.52,
        n=500,
    )

    # Configurações do plano
    plane = Plane(
        point=Point(0, -2, 0),
        normal=Vector(0, 1, 0),
        color=np.array([0, 1, 1]),  # Cor do plano (amarelo)
        k_ambient=0.3,
        k_diffuse=0.5,
        k_specular=0.8,
        k_reflection=0.0,
        k_refraction=0.0,
        refraction_index=1.52,
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
        refraction_index=1.5,
        n=30,
    )

    matrix = translate(-10, -10, 0)
    meshTransformerd = apply_affine_transformation(mesh, matrix)

    # for vertex in triangleTransformed.vertice_list:
    # print(f"vertex {vertex.array()}")

    objects = [sphere1, sphere2, sphere3, plane]

    # Luzes
    light1 = Light(Point(100, 300, 50), np.array([255, 255, 255]))
 
    lights = [light1]
    ambiental_color_light = np.array([50, 50, 50])
    # Cria o renderizador
    renderer = Renderer(camera, objects, lights, ambiental_color_light)
    renderer.render()


if __name__ == "__main__":
    main()
