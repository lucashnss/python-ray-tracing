import numpy as np
from light import Light

from objects.bezier_surface import BezierSurface  # certifique-se que o nome e o caminho do arquivo estão corretos

from camera import Camera
from renderer import Renderer
from point import Point
from vector import Vector


def main():
    # Configurações da câmera
    camera = Camera(
        camera_point=Point(3, 0, 1),
        target_point=Point(0, 0, 1),
        vector_up=Vector(0, 0, 1),
        target_distance=1,
        hres=500,
        vres=500,
    )

    # Pontos de controle da superfície de Bézier (4x4)
    # Pontos de controle (3x3) para uma superfície quadrática
    # control_points = [
    #     [Point(x, y, np.cos(x * y)) for y in np.linspace(-1, 1, 3)]
    #     for x in np.linspace(-1, 1, 3)
    # ]    
    # control_points = [
    #     [Point(-1.5, -1.5, 0), Point(-0.5, -1.5, 0.2), Point(0.5, -1.5, 0.2), Point(1.5, -1.5, 0)],
    #     [Point(-1.5, -0.5, 0.2), Point(-0.5, -0.5, 0.7), Point(0.5, -0.5, 0.7), Point(1.5, -0.5, 0.2)],
    #     [Point(-1.5,  0.5, 0.2), Point(-0.5,  0.5, 0.7), Point(0.5,  0.5, 0.7), Point(1.5,  0.5, 0.2)],
    #     [Point(-1.5,  1.5, 0), Point(-0.5,  1.5, 0.2), Point(0.5,  1.5, 0.2), Point(1.5,  1.5, 0)],
    # ]

    control_points = [
        [Point(-1.5, -1.5, 0), Point(-0.5, -1.5, 0.2), Point(0.5, -1.5, 0.2), Point(1.5, -1.5, 0)],
        [Point(-1.5, -0.5, 0.2), Point(-0.5, -0.5, 3), Point(0.5, -0.5, 0.6), Point(1.5, -0.5, 0.2)],
        [Point(-1.5,  0.5, 0.2), Point(-0.5,  0.5, 3), Point(0.5,  0.5, 0.6), Point(1.5,  0.5, 0.2)],
        [Point(-1.5,  1.5, 0), Point(-0.5,  1.5, 0.2), Point(0.5,  1.5, 0.2), Point(1.5,  1.5, 0)],
    ]
 
    bezier_surface = BezierSurface(
        control_points=control_points,
        resolution=15,  # aumenta se quiser uma malha mais densa
        color=np.array([100, 200, 255]),
        k_ambient=0.1,
        k_diffuse=0.6,
        k_specular=0.4,
        k_reflection=0.0,
        k_refraction=0.0,
        refraction_index=1.0,
        n=15,
    )

    # Lista de objetos da cena
    objects = [bezier_surface]

    # Luzes
    light1 = Light(Point(0, 100, 100), np.array([255, 255, 255]))
    lights = [light1]
    ambiental_color_light = np.array([0, 0, 0])

    # Renderizador
    renderer = Renderer(camera, objects, lights, ambiental_color_light)
    renderer.render()


if __name__ == "__main__":
    main()
