# import sys


class Vertex:
    """Base Vertex class for Graph vertices.

    Stores actual identity of each vertex.
    """

    def __init__(self, vertex_id):
        self.vertex_id = vertex_id
        self.neighbours = dict()

    def add_neighbour(self, new_neighbour, weight=0):
        self.neighbours[new_neighbour] = weight

    def get_neighbours(self):
        return self.neighbours.keys()

    def remove_neighbour(self, neighbour):
        self.neighbours.pop(neighbour, None)


class Graph:
    """Base Graph class."""

    def __init__(self):
        self.vertices = dict()
        self.vertex_count = 0

    def add_vertex(self, vertex_id):
        self.vertices[vertex_id] = Vertex(vertex_id)
        self.vertex_count += 1

    def remove_vertex(self, vertex_id):
        self.vertices.pop(vertex_id, None)
        self.vertex_count -= 1

    def get_vertex(self, vertex_id):
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            return None

    def add_edge(self, vertex1, vertex2, weight=0):
        if vertex1 in self.vertices and vertex2 in self.vertices:
            vertex1.add_neighbour(vertex2, weight)
            vertex2.add_neighbour(vertex1, weight)
        else:
            return

    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.vertices and vertex2 in self.vertices:
            vertex1.remove_neighbour(vertex2)
            vertex2.remove_neighbour(vertex1)
