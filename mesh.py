class Mesh:
    def __init__(self, n_triangles, n_vertices, vertice_list, triples_list, normal_list, 
                 vertices_normal_list, colors_normalized_list):
        self.n_triangles = n_triangles
        self.n_vertices = n_vertices
        self.vertice_list = vertice_list
        self.triples = triples_list
        self.normal_list = normal_list
        self.vertices_normal_list = vertices_normal_list
        self.colors_normalized_list = colors_normalized_list
    

        def __str__(self):
            return f"Mesh: {self.n_triangles} {self.n_vertices} 
            {self.vertice_list} {self.triples} {self.normal_list} 
            {self.vertices_normal_list} {self.colors_normalized_list}"
        
        def intersect_mesh(self):
            pass