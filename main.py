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




    sphere = Sphere(center=Point(-3, -3.5, -2), radius=1.5, color=(255,0,0))

    triangle = Mesh(n_triangles=3,
                    n_vertices=8,
                    vertice_list=[Point(5, 0, -10),
                                  Point(2, 0, -10),
                                  Point(2, 5, -10),
                                  Point(-5,0,-10),
                                  Point(-5,5,-10),
                                  Point(5, 0, -15),
                                  Point(-5,0,-15),
                                  Point(-5,5,-15), ],
                    triples_list=[(0, 1, 2),
                                  (2, 3, 4),
                                  (5, 6, 7)],
                    normal_list=[Vector(0, 0, 1),
                                 Vector(0, 0, 1),
                                 Vector(0, 0, 1),
                                 Vector(0, 0, 1)],
                    vertices_normal_list=[Vector(0, 0, 1), Vector(0, 0, 1), Vector(0, 0, 1)],
                    colors_normalized_list=[(0,255,0), (255,255,0), (0,255,255)], color=(255,255,255))






    objects = [triangle, sphere]
    renderer = Renderer(camera, objects, hres=500, vres=500)
    renderer.render()



if __name__ == "__main__":
    main()
