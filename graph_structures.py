class Vertex:
    def __init__(self):
        self.neighbours = list()
        self.visited = False


class Graph:
    def __init__(self):
        self.vertices = list()

        self.to_search = Stack()
        self.visited = Set()

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def get_vertex_count(self):
        return len(self.vertices)
