from app.graph import Graph
import heapq

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
    calculate_distance = distances[current] + weight

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
    # Retrieve all locations in the graph
    locations = graph.get_locations()

    # Check that start and end locations are in the graph
    if start not in locations:
        raise ValueError("Start location is not in the graph")
    
    if end not in locations:
        raise ValueError("End location is not in the graph")

    # Check if the start and end locations are the same
    if start == end:
        return ([start], 0)
    
    # Initialize distances and previous dictionaries
    distances = {}
    for location in locations:
        distances[location] = float('inf')

    # Set initial distance for the start location to 0
    distances[start] = 0.0

    previous = {}
    for location in locations:
        previous[location] = None

    priority_queue = []
    heapq.heappush(priority_queue, (0.0, start))

    # Dijkstra's algorithm main loop
    while priority_queue:
        current_distance, current_location = heapq.heappop(priority_queue)

        # If the distance is greater than the recorded distance, skip processing
        if current_distance > distances[current_location]:
            continue

        # If we reached the end location, we can stop
        if current_location == end:
            break

        # Get neighbors of the current location
        neighbors = graph.get_neighbors(current_location)

        for neighbor, road in neighbors.items():
            if not road.is_open:
                continue

            if relax_edge(
                current_location,
                neighbor,
                road.travel_time,
                distances,
            ):
                previous[neighbor] = current_location
                heapq.heappush(
                    priority_queue,
                    (distances[neighbor], neighbor),
                )

    # Check if no path was found
    if distances[end] == float('inf'):
        return ([], float('inf'))

    # Reconstruct the shortest path from start to end
    path = []
    current_location = end
    while current_location is not None:
        path.append(current_location)
        current_location = previous[current_location]

    # Reverse the path to get it from start to end and return it along with the total travel time
    path.reverse()
    return (path, distances[end])