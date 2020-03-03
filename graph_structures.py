class Vertex:
    def __init__(self):
        self.neighbours = []


class Graph:
    def __init__(self):
        self.vertices = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def get_vertex_count(self):
        return len(self.vertices)
