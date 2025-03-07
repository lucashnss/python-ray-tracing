from typing import List
import numpy as np
from plane import Plane
from point import Point
from ray import Ray
from vector import Vector


class Mesh:
    def __init__(self, n_triangles: int, n_vertices: int, vertice_list: List[Point], triples_list,
                 normal_list: List[Vector], vertices_normal_list: List[Vector], colors_normalized_list, color,
                 k_ambient, k_diffuse, k_specular, k_reflection, k_refraction, refraction_index, n):
        self.type =  "Mesh"
        self.n_triangles = n_triangles
        self.n_vertices = n_vertices
        self.vertice_list = vertice_list
        self.triples_list = triples_list
        self.normal_list = normal_list
        self.vertices_normal_list = vertices_normal_list
        self.colors_normalized_list = colors_normalized_list
        self.color = color
        self.k_ambient = k_ambient
        self.k_diffuse = k_diffuse
        self.k_specular = k_specular
        self.k_reflection = k_reflection
        self.k_refraction = k_refraction
        self.IOR = refraction_index
        self.n = n

    def __str__(self):
        return f"Mesh: {self.n_triangles}, {self.n_vertices}, {self.vertice_list}, {self.triples}, {self.normal_list}, {self.vertices_normal_list}, {self.colors_normalized_list}"


    def intersect_triangle_plane(self, vertices: List[Point], ray: Ray, triangle_normal: Vector):
        [v0, v1, v2] = vertices

        a0: Vector = v1 -  v0 # aresta 0 (vetor)
        a1: Vector = v2 - v0 # aresta 1 (vetor)


        normal = a0.cross_product(a1)
        plane = Plane(v0, normal, (0, 0, 255)) # plano do triângulo
        t = plane.intersect(ray)

    # intersecção do raio com o plano
        if t is None:
            return None

        P =  ray.origin + ray.direction.scale(t)
        a2 = P - v0

        # Construindo a matriz e o vetor para resolver o sistema linear
        M = np.array([[a0.dot_product(a0), a0.dot_product(a1)],
                    [a0.dot_product(a1), a1.dot_product(a1)]])
        b = np.array([a2.dot_product(a0), a2.dot_product(a1)])

        # Resolvendo o sistema linear M * [v, w] = b
        barycentric_coords = np.linalg.solve(M, b)


        alpha, beta = barycentric_coords
        gamma = 1 - alpha - beta

        if 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1:
            return t  # Ponto de interseção válido

        return None  # Interseção fora do triângulo

    def intersect(self, ray: Ray):

        closest_t = float('inf')
        for index in range(self.n_triangles):

            triple = self.triples_list[index]
            vertices = [self.vertice_list[i] for i in triple]

            t = self.intersect_triangle_plane(vertices, ray, self.normal_list[index])
            color = self.colors_normalized_list[index]
            if t and t < closest_t:
                self.color = color
                closest_t = t

        return closest_t

def apply_affine_transformation(mesh: Mesh, transformation_matrix: np.ndarray) -> Mesh:
    vertice_list_transformed: List[Point] = []
    for vertex in mesh.vertice_list:
        result = np.matmul(transformation_matrix, [vertex.x, vertex.y, vertex.z, 1])
        vertice_list_transformed.append(Point(result[0], result[1], result[2]))

    return Mesh(mesh.n_triangles, mesh.n_vertices, vertice_list_transformed.copy(), mesh.triples_list, mesh.normal_list,
                mesh.vertices_normal_list, mesh.colors_normalized_list, mesh.color)
