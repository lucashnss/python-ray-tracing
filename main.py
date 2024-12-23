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
        camera_point=Point(0, 0, -1), 
        target_point=Point(0, 0, 0), 
        vector_up=Vector(0, 1, 0), 
        hres=800, 
        vres=600
    )
    print(camera)

    # Criar objetos
    s1 = Sphere(center=Point(2,-5,10), radius=1, color=(0,0,255))
    s2 = Sphere(center=Point(-2,-5,10), radius=1, color=(255,0,0))
    s3 = Sphere(center=Point(-2,2,10), radius=1, color=(255,255,255))
    plane = Plane(point=Point(10,0,0), normal=Vector(-1,0,0), color=(0,255,0))
    # Renderizar a cena
    renderer = Renderer(camera, [s1, s2, s3, plane], hres=800, vres=600)
    renderer.render()


if __name__ == "__main__":
    main()
