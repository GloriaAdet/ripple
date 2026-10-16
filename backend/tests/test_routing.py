import pytest
from app.graph import Graph
from app.routing import dijkstra

# Find the shortest route from start to end
def test_shortest_route():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_location("C")
    graph.add_location("D")
    graph.add_location("E")
    graph.add_location("F")

    graph.add_road("A", "B", 4.0)
    graph.add_road("A", "C", 7.0)
    graph.add_road("B", "D", 3.0)
    graph.add_road("B", "E", 6.0)
    graph.add_road("C", "E", 2.0)
    graph.add_road("D", "E", 4.0)
    graph.add_road("E", "F", 5.0)

    path, travel_time = dijkstra(graph, "A", "F")
    assert path == ["A", "C", "E", "F"]
    assert travel_time == 14.0

# Test a route where the start and end locations are the same
def test_same_start_end():
    graph = Graph()
    graph.add_location("A")
    path, travel_time = dijkstra(graph, "A", "A")
    assert path == ["A"]
    assert travel_time == 0.0

# Create a graph with an isolated location and attempt to route to it
def test_isolated_location():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_location("C")
    graph.add_road("A", "B", 5.0)

    path, travel_time = dijkstra(graph, "A", "C")
    assert path == []
    assert travel_time == float("inf")

# Request a route from an unknown start location
def test_unknown_start_location():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    with pytest.raises(ValueError):
        dijkstra(graph, "C", "B")

# Request a route to an unknown end location
def test_unknown_end_location():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    with pytest.raises(ValueError):
        dijkstra(graph, "A", "C")

# Request a route where two locatoins connected by a road with zero travel time
def test_zero_travel_time():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_road("A", "B", 0.0)

    path, travel_time = dijkstra(graph, "A", "B")
    assert path == ["A", "B"]
    assert travel_time == 0.0

# Request a route where there are multiple paths with the same total travel time
def test_multiple_paths_same_travel_time():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_location("C")
    graph.add_location("D")

    graph.add_road("A", "B", 5.0)
    graph.add_road("A", "C", 5.0)
    graph.add_road("B", "D", 5.0)
    graph.add_road("C", "D", 5.0)

    path, travel_time = dijkstra(graph, "A", "D")
    assert travel_time == 10.0
    assert path in [["A", "B", "D"], ["A", "C", "D"]]

# Request a route where a longer path is found first but a shorter path is found later
def test_longer_path_found_first():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_location("C")
    graph.add_location("D")

    graph.add_road("A", "B", 10.0)
    graph.add_road("A", "C", 1.0)
    graph.add_road("C", "D", 1.0)
    graph.add_road("D", "B", 1.0)

    path, travel_time = dijkstra(graph, "A", "B")
    assert path == ["A", "C", "D", "B"]
    assert travel_time == 3.0