from typing import List
import numpy as np
from plane import Plane
from point import Point
from ray import Ray
from vector import Vector


class Mesh:
    def __init__(self, n_triangles: int, n_vertices: int, vertice_list: List[Point], triples_list, normal_list: List[Vector], vertices_normal_list, colors_normalized_list, color):
        self.n_triangles = n_triangles
        self.n_vertices = n_vertices
        self.vertice_list = vertice_list
        self.triples = triples_list
        self.normal_list = normal_list
        self.vertices_normal_list = vertices_normal_list
        self.colors_normalized_list = colors_normalized_list
        self.color = color

    def __str__(self):
        return f"Mesh: {self.n_triangles}, {self.n_vertices}, {self.vertice_list}, {self.triples}, {self.normal_list}, {self.vertices_normal_list}, {self.colors_normalized_list}"


    def intersect_triangle_plane(self, vertices: List[Point], ray: Ray, triangle_normal: Vector):
        [v0, v1, v2] = vertices
        a0: Vector = v1 -  v0 # aresta 0 (vetor)
        a1: Vector = v2 - v0 # aresta 1 (vetor)

        plane = Plane(v0, triangle_normal, (0, 0, 255)) # plano do triângulo
        t = plane.intersect(ray)

    # intersecção do raio com o plano
        if t is None:
            return None


        P =  ray.origin + ray.direction.scale(t)
        S = P - v0

        M = np.array([[a0.x, a1.x], [a0.y, a1.y]])



        barycentric_coords = np.linalg.solve(M, [S.x, S.y])

        alpha, beta = barycentric_coords
        gamma = 1 - alpha - beta

        if 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1:
            return t  # Ponto de interseção válido

        return None  # Interseção fora do triângulo

    def intersect(self, ray: Ray):


        vertices = [self.vertice_list[i] for i in self.triples[0]]

        t = self.intersect_triangle_plane(vertices, ray, self.normal_list[0])


        if t is not None:
            return t
