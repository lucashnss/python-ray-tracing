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
from transform import affine_transform, translate
from bezier_surface import BezierSurface


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
    control_points = [
        [Point(-1.5, -1.5, 0), Point(-0.5, -1.5, 0), Point(0.5, -1.5, 0), Point(1.5, -1.5, 0)],
        [Point(-1.5, -0.5, 0), Point(-0.5, -0.5, 1), Point(0.5, -0.5, 1), Point(1.5, -0.5, 0)],
        [Point(-1.5,  0.5, 0), Point(-0.5,  0.5, 1), Point(0.5,  0.5, 1), Point(1.5,  0.5, 0)],
        [Point(-1.5,  1.5, 0), Point(-0.5,  1.5, 0), Point(0.5,  1.5, 0), Point(1.5,  1.5, 0)],
    ]

    bezier_surface = BezierSurface(
        control_points=control_points,
        color=(255, 0, 0),           # Red surface
        k_ambient=0.1,
        k_diffuse=0.6,
        k_specular=0.3,
        k_reflection=0.0,
        k_refraction=0.0,
        refraction_index=1.0,
        n=500                        # Specular exponent
    )

    objects = [bezier_surface]

    # Luzes
    light1 = Light(Point(0, 100, 100), np.array([255, 255, 255]))

    lights = [light1]
    ambiental_color_light = np.array([0, 0, 0])
    # Cria o renderizador
    renderer = Renderer(camera, objects, lights, ambiental_color_light)
    renderer.render()


if __name__ == "__main__":
    main()
