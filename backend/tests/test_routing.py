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

# Test a route where there is a road closure, and then the road reopens
def test_reroutes_when_road_closes():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_location("C")

    graph.add_road("A", "B", 4.0)
    graph.add_road("A", "C", 3.0)
    graph.add_road("C", "B", 3.0)

    # Initially, the shortest path from A to B is a direct road with a travel time of 4.0
    path, travel_time = dijkstra(graph, "A", "B")
    assert path == ["A", "B"]
    assert travel_time == 4.0

    # Now, simulate a road closure by setting the road from A to B as closed
    road_ab = graph.get_neighbors("A")["B"]
    road_ab.close()

    # After the road closure, the shortest path from A to B should be A->C->B with a total travel time of 6.0
    path, travel_time = dijkstra(graph, "A", "B")
    assert path == ["A", "C", "B"] 
    assert travel_time == 6.0

    # Reopen the path from A to B
    road_ab.reopen()
    path, travel_time = dijkstra(graph, "A", "B")
    assert path == ["A", "B"]
    assert travel_time == 4.0
    
# Test where all roads are closed, and the algorithm should return an empty path and infinite travel time
def test_all_roads_closed():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_location("C")

    graph.add_road("A", "B", 4.0)
    graph.add_road("A", "C", 3.0)
    graph.add_road("C", "B", 3.0)

    # Close all roads that connect to B
    graph.get_neighbors("A")["B"].close()
    graph.get_neighbors("C")["B"].close()

    # Now, there should be no available path from A to B
    path, travel_time = dijkstra(graph, "A", "B")
    assert path == []
    assert travel_time == float('inf')

# Test road clossure works in both directions, and the algorithm should return an empty path and infinite travel time
def test_bidirectional_road_closure():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")

    graph.add_road("A", "B", 4.0)

    # Close the road from A to B
    graph.get_neighbors("A")["B"].close()

    # Now, there should be no available path from A to B
    path, travel_time = dijkstra(graph, "A", "B")
    assert path == []
    assert travel_time == float('inf')

    # Also, there should be no available path from B to A
    path, travel_time = dijkstra(graph, "B", "A")
    assert path == []
    assert travel_time == float('inf')

# Test that the algorithm reroutes when an open road's travel time increases
def test_dijkstra_reroutes_when_open_road_travel_time_increases():
    graph = Graph()
    for location in ("A", "B", "C", "D"):
        graph.add_location(location)

    graph.add_road("A", "B", 1)
    graph.add_road("B", "D", 1)
    graph.add_road("A", "C", 2)
    graph.add_road("C", "D", 2)

    assert dijkstra(graph, "A", "D") == (["A", "B", "D"], 2)

    graph.update_road("B", "D", 5)

    assert graph.get_neighbors("B")["D"].is_open is True
    assert dijkstra(graph, "A", "D") == (["A", "C", "D"], 4)