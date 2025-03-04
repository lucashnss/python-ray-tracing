from mesh import Mesh
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
        camera_point=Point(0, 0, 5),
        target_point=Point(0, 0, 0),
        vector_up=Vector(0, 1, 0),
        target_distance=1,
        hres=500,
        vres=500
    )


    # Criar objetos

    # Novas esferas

    sphere4 = Sphere(center=Point(2, -4.5, -2), radius=0.5, color=(0, 0, 255))
    sphere5 = Sphere(center=Point(0, -4, -2), radius=1, color=(0,255,0))
    sphere6 = Sphere(center=Point(-3, -3.5, -2), radius=1.5, color=(255,0,0))


    # Novos planos
    plane3 = Plane(point=Point(5, 0, 0), normal=Vector(-1, 0, 0), color=(0,255,0))
    plane4 = Plane(point=Point(-5, 0, 0), normal=Vector(1, 0, 0), color=(0, 0, 255))
    plane5 = Plane(point=Point(0, -5, 0), normal=Vector(0, 1, 0), color=(255,255,255))
    plane6 = Plane(point=Point(0, 5, 0), normal=Vector(0, -1, 0), color=(255,255,255))
    plane7 = Plane(point=Point(0, 0, -5), normal=Vector(0, 0, 1), color=(255,255,255))
    plane8 = Plane(point=Point(0, 0, 6), normal=Vector(0, 0, -1), color=(255,255,255))


    triangle = Mesh(n_triangles=1, n_vertices=3, vertice_list=[Point(5, 0, 0), Point(0, 5, 0) ,Point(-5, -5, 0) ], triples_list=[(0, 1, 2)], normal_list=[Vector(0, 0, 1)], vertices_normal_list=[Vector(0, 0, 1), Vector(0, 0, 1), Vector(0, 0, 1)], colors_normalized_list=[(0,255,0)], color=(0,255,0))






    objects = [triangle, sphere6]
    renderer = Renderer(camera, objects, hres=500, vres=500)
    renderer.render()



if __name__ == "__main__":
    main()
