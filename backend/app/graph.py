from app.road import Road

class Graph:
    # A graph represented as an adjacency list
    def __init__(self):
        self._adjacency_list: dict[str, dict[str, Road]] = {}

    # Add a location to the graph
    def add_location(self, location: str) -> None:
        if location not in self._adjacency_list:
            self._adjacency_list[location] = {}

    # Add a road between two locations
    def add_road(
            self,
            start: str,
            end: str,
            travel_time: float
    ) -> None:
        
        # Validate that start and end locations are in the graph
        if start not in self._adjacency_list:
            raise ValueError("Start location is not in the graph")
        if end not in self._adjacency_list:
            raise ValueError("End location is not in the graph")

        road = Road(start, end, travel_time)

        self._adjacency_list[start][end] = road
        self._adjacency_list[end][start] = road

    # Get the neighbors of a location along with travel times
    def get_neighbors(self, location: str) -> dict[str, Road]:

        # Raise error if location is not in the graph
        if location not in self._adjacency_list:
            raise ValueError("Location is not in the graph")
        
        return self._adjacency_list[location].copy()

    def get_locations(self) -> list[str]:
        return list(self._adjacency_list.keys())

    def close_road(self, start: str, end: str) -> None:
        # Validate that the road exists with get_road method
        road = self._get_road(start, end)
        road.close()

    def reopen_road(self, start: str, end: str) -> None:
        # Validate that the road exists with get_road method
        road = self._get_road(start, end)
        road.reopen()

    def update_road(self, start: str, end: str, travel_time: float) -> None:
        # Retrieve the existing road
        road = self._get_road(start, end)
        # Update its travel time
        road.update_travel_time(travel_time)

    # Helpers
    def _get_road(self, start: str, end: str) -> Road:
        # Validate that the road exists
        if start not in self._adjacency_list or end not in self._adjacency_list[start]:
            raise ValueError("Road does not exist in the graph")
        # Return the existing Road object
        return self._adjacency_list[start][end]

    