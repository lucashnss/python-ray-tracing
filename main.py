from obj_reader import ObjReader
from camera import Camera
from point import Point
from vector import Vector
# Divirtam-se :)

def main():
    camera = Camera(camera_point=Point(0, 0, 0), target_point=Point(0, 0, 1), vector_up=Vector(0, 1, 0), width=300, height=300)
    print(camera)
    camera.ray_casting([], 2000)



if __name__ == "__main__":
    main()
