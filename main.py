from obj_reader import ObjReader
from camera import Camera
from renderer import Renderer
from point import Point
from vector import Vector
from sphere import Sphere
from plane import Plane

# Divirtam-se :)

def main():
    # Configurações de câmera
    camera = Camera(
        camera_point=Point(0, 0, -5),
        target_point=Point(0, 0, 0),
        vector_up=Vector(0, 1, 0),
        target_distance=1,
        hres=800,
        vres=600
    )
    print(camera)

    # Criar objetos
    sphere = Sphere(center=Point(-2,-5,2), radius=3, color=(255,0,0))
    sphere2 = Sphere(center=Point(5,-5, 2), radius=1, color=(0,0,255))

    sphere3 = Sphere(center=Point(5,5, 2), radius=2.5, color=(0,100,255))
    plane = Plane(point=Point(10,0,0), normal=Vector(-1,0,0), color=(0,255,0))
    plane2 = Plane(point=Point(-10,0,0), normal=Vector(2,0,0), color=(255,255,0))



    # Renderizar a cena
    renderer = Renderer(camera, [sphere,  sphere2,  sphere3, plane, plane2], hres=800, vres=600)
    renderer.render()


if __name__ == "__main__":
    main()
