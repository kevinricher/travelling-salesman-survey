import graph_structures


class TestGraphStructures:
    def test_vertex_manipulation(self):
        graph = graph_structures.Graph()
        for i in range(3):
            graph.add_vertex(graph_structures.Vertex())
        assert graph.get_vertex_count() == 3
