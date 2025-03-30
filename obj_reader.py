from point import Point
from vector import Vector
from color_map import Colormap
import os

class Face:
    def __init__(self):
        self.vertice_indices = [0, 0, 0]
        self.normal_indices = [0, 0, 0]
        self.ka = Vector(0, 0, 0)
        self.kd = Vector(0, 0, 0)
        self.ks = Vector(0, 0, 0)
        self.ke = Vector(0, 0, 0)
        self.ns = 0
        self.ni = 0
        self.d = 0

class ObjReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.vertices = []
        self.normals = []
        self.faces = []
        self.colormap = None
        self.read_file()

    def read_file(self):
        try:
            with open(self.file_path, 'r') as file:
                current_material = None
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    parts = line.split()
                    if parts[0] == 'v':
                        self.vertices.append(Point(float(parts[1]), float(parts[2]), float(parts[3])))
                    elif parts[0] == 'vn':
                        self.normals.append(Vector(float(parts[1]), float(parts[2]), float(parts[3])))
                    elif parts[0] == 'f':
                        face_data = []
                        for part in parts[1:]:
                            vertex_data = part.split('/')
                            vertex_index = int(vertex_data[0]) - 1
                            normal_index = int(vertex_data[2]) - 1 if len(vertex_data) > 2 else 0 #Adicionado verificação para ver se a normal existe.

                            face_data.append((vertex_index, normal_index))

                        face = Face()
                        face.vertice_indices = [face_data[0][0], face_data[1][0], face_data[2][0]]
                        face.normal_indices = [face_data[0][1], face_data[1][1], face_data[2][1]]

                        if current_material and self.colormap:
                            material = self.colormap.get_material(current_material)
                            face.ka = material.ka
                            face.kd = material.kd
                            face.ks = material.ks
                            face.ke = material.ke
                            face.ns = material.ns
                            face.ni = material.ni
                            face.d = material.d

                        self.faces.append(face)
                    elif parts[0] == 'usemtl':
                        current_material = parts[1]
                    elif parts[0] == 'mtllib':
                        mtl_file = os.path.join(os.path.dirname(self.file_path), parts[1])
                        self.colormap = Colormap(mtl_file)

        except FileNotFoundError:
            print(f"Arquivo não encontrado: {self.file_path}")

    def get_faces(self):
        return self.faces

    def get_vertices(self):
        for (enum, vertex) in enumerate(self.vertices):
            print(f"Vertex {enum}: ({vertex.x}, {vertex.y}, {vertex.z})")

    def print_faces(self):
        for (enum, face) in enumerate(self.faces):
            print(f"Face {enum}:")
            print(f"Vertices: {face.vertice_indices}")
            print(f"Normals: {face.normal_indices}")
            print(f"Ka: {face.ka}")
            print(f"Kd: {face.kd}")
            print(f"Ks: {face.ks}")
            print(f"Ke: {face.ke}")
            print(f"Ns: {face.ns}")
            print(f"Ni: {face.ni}")
            print(f"d: {face.d}")
            print()

if __name__ == "__main__":
    reader = ObjReader("inputs/icosahedron.obj")
    reader.read_file()

    vertices = reader.get_vertices()
    faces = reader.get_faces()

    print("Vertices:", vertices)
    print("Faces:")
    reader.print_faces()