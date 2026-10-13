import pytest
from app.graph import Graph

def test_add_location():
    graph = Graph()
    graph.add_location("A")
    assert graph.get_neighbors("A") == {}

def test_add_duplicate_location():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_road("A", "B", 10.0)

    graph.add_location("A")

    assert graph.get_neighbors("A") == {"B": 10.0}
    assert graph.get_neighbors("B") == {"A": 10.0}

def test_add_bidirectional_road():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_road("A", "B", 10.0)
    assert graph.get_neighbors("A") == {"B": 10.0}
    assert graph.get_neighbors("B") == {"A": 10.0}

def test_update_road():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_road("A", "B", 10.0)
    graph.add_road("A", "B", 15.0)  # This should update the existing road
    assert graph.get_neighbors("A") == {"B": 15.0}
    assert graph.get_neighbors("B") == {"A": 15.0}

    with pytest.raises(ValueError):
        graph.add_road("A", "Z", 3.0)

def test_negative_travel_time():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")

    with pytest.raises(ValueError):
        graph.add_road("A", "B", -5.0)

    assert graph.get_neighbors("A") == {}
    assert graph.get_neighbors("B") == {}

def test_nonfinite_travel_time():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")

    with pytest.raises(ValueError):
        graph.add_road("A", "B", float("inf"))

def test_nan_travel_time():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")

    with pytest.raises(ValueError):
        graph.add_road("A", "B", float("nan")) 

def test_nonexistent_location():
    graph = Graph()

    with pytest.raises(ValueError):
        graph.get_neighbors("A")

def test_self_connection():
    graph = Graph()
    graph.add_location("A")

    with pytest.raises(ValueError):
        graph.add_road("A", "A", 10.0)

def test_unknown_location():
    graph = Graph()
    graph.add_location("A")

    # Unknown destination
    with pytest.raises(ValueError):
        graph.add_road("A", "Z", 5)

    # Unknown starting location
    with pytest.raises(ValueError):
        graph.add_road("Z", "A", 5)

    # Neither operation should create Z
    with pytest.raises(ValueError):
        graph.get_neighbors("Z")

    assert graph.get_neighbors("A") == {}

def test_graph_state_after_returned_neighbors():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_road("A", "B", 10.0)
    neighbors = graph.get_neighbors("A")
    assert neighbors == {"B": 10.0}
    # Ensure the internal state is not modified
    neighbors["B"] = 999
    assert graph.get_neighbors("A") == {"B": 10.0}
    assert graph.get_neighbors("B") == {"A": 10.0}

def test_state_preservation():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_road("A", "B", 4)

    # Ensure that after attempting to overwrite the travel time with a bad value, the original value still remains
    with pytest.raises(ValueError):
        graph.add_road("A", "B", -10.0)
    assert graph.get_neighbors("A") == {"B": 4}
    assert graph.get_neighbors("B") == {"A": 4}

    def test_zero_travel_time():
        graph = Graph()
        graph.add_location("A")
        graph.add_location("B")

        graph.add_road("A", "B", 0)

        assert graph.get_neighbors("A") == {"B": 0}
        assert graph.get_neighbors("B") == {"A": 0}