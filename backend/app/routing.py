from app.graph import Graph

def relax_edge(
        current: str,
        neighbor: str,
        weight: float,
        distances: dict[str,float]
) -> bool:

    """
    Update the neighbor's distance if a shorter route
    through current has been found

    Return True if updated, otherwise, return false
    """
    calculate_distance = distances[current] + weight;

    if calculate_distance < distances[neighbor]:
        distances[neighbor] = calculate_distance
        return True
    return False

def dijkstra(
        graph: Graph, 
        start: str, 
        end: str
        ) -> tuple[list[str], float]:

    """
    Return shortest path and total travel time
    between start location and end location
    """

    # Initialize distances for each location
    distances = {}

    pass