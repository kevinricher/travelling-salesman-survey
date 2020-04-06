import pytest
import graph


@pytest.fixture(scope="function")
def test_graph():
    return graph.Graph()


class TestGraph:
    """Test graph creation methods."""

    def test_vertex_creation(self, test_graph):
        assert test_graph.vertex_count == 0
        test_graph.add_vertex(1)
        assert test_graph.vertex_count == 1
        test_graph.add_vertex('a')

    def test_vertex_deletion(self, test_graph):
        test_graph.add_vertex('ab')
        test_graph.add_vertex('ba')
        test_graph.remove_vertex('ab')
        assert test_graph.vertex_count == 1
        assert test_graph.get_vertex('ba') is not None

    def test_vertex_membership(self, test_graph):
        test_graph.add_vertex('a')
        assert test_graph.get_vertex('a').vertex_id == 'a'
