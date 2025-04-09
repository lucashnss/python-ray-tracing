import numpy as np
from point import Point
from vector import Vector
from .mesh import Mesh
from typing import List
from math import comb

def bernstein_poly(i, n, t):
    return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

def bezier_patch(control_points, u, v):
    m = len(control_points) - 1
    n = len(control_points[0]) - 1
    p = Point(0, 0, 0)
    for i in range(m + 1):
        for j in range(n + 1):
            b_ij = bernstein_poly(i, m, u) * bernstein_poly(j, n, v)
            p += control_points[i][j] * b_ij
    return p

def compute_normal(p1: Point, p2: Point, p3: Point) -> Vector:
    return ((p2 - p1).cross_product(p3 - p1)).normalize()

class BezierSurface(Mesh):
    def __init__(self, control_points: List[List[Point]], resolution: int,
                 color: np.ndarray, k_ambient: float, k_diffuse: float, k_specular: float,
                 k_reflection: float, k_refraction: float, refraction_index: float, n: int):
        
        self.control_points = control_points
        self.resolution = resolution

        # Gera a grade de pontos amostrados
        vertices = []
        for i in range(resolution + 1):
            u = i / resolution
            for j in range(resolution + 1):
                v = j / resolution
                vertices.append(bezier_patch(control_points, u, v))

        # Constrói os triângulos conectando os pontos da malha
        triples = []
        normals = []
        colors = []
        for i in range(resolution):
            for j in range(resolution):
                idx = i * (resolution + 1) + j
                v0 = idx
                v1 = idx + 1
                v2 = idx + resolution + 1
                v3 = idx + resolution + 2

                # Triângulo 1
                triples.append((v0, v1, v2))
                normals.append(compute_normal(vertices[v0], vertices[v1], vertices[v2]))
                colors.append(color / 255.0)

                # Triângulo 2
                triples.append((v1, v3, v2))
                normals.append(compute_normal(vertices[v1], vertices[v3], vertices[v2]))
                colors.append(color / 255.0)

        # Lista de normais por vértice (opcional aqui)
        vertex_normals = [Vector(0, 1, 0)] * len(vertices)

        # Cria o Mesh com os dados gerados

        print("Criação da malha de Bézier concluída.")
        print("Número de triângulos: ", len(triples))
        print("Número de vértices: ", len(vertices))
        super().__init__(
            n_triangles=len(triples),
            n_vertices=len(vertices),
            vertice_list=vertices,
            triples_list=triples,
            normal_list=normals,
            vertices_normal_list=vertex_normals,
            colors_normalized_list=colors,
            color=color,
            k_ambient=k_ambient,
            k_diffuse=k_diffuse,
            k_specular=k_specular,
            k_reflection=k_reflection,
            k_refraction=k_refraction,
            refraction_index=refraction_index,
            n=n
        )

        self.type = "BezierSurface"
