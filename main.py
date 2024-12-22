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
        hres=800, 
        vres=600
    )
    print(camera)

    # Criar objetos
    sphere = Sphere(center=Point(0,0,5), radius=1, color=(255,0,0))
    plane = Plane(point=Point(0,-1,0), normal=Vector(0,1,0), color=(0,255,0))

    # Renderizar a cena
    renderer = Renderer(camera, [sphere, plane], hres=800, vres=600)
    renderer.render()


if __name__ == "__main__":
    main()
