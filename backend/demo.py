from app.graph import Graph

graph = Graph()

for location in ["A", "B", "C", "D", "E", "F"]:
    graph.add_location(location)

roads = [
    ("A", "B", 4),
    ("A", "C", 7),
    ("B", "D", 3),
    ("B", "E", 6),
    ("C", "E", 2),
    ("D", "E", 4),
    ("E", "F", 5),
]

for start, end, travel_time in roads:
    graph.add_road(start, end, travel_time)

for location in ["A", "B", "C", "D", "E", "F"]:
    print(location, graph.get_neighbors(location))