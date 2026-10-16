import math
from app.road import Road

class Graph:
    # A graph represented as an adjacency list
    def __init__(self):
        self._adjacency_list: dict[str, dict[str, float]] = {}

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
        road = Road(start, end, travel_time)

        if start not in self._adjacency_list:
            raise ValueError("Start location is not in the graph")
        if end not in self._adjacency_list:
            raise ValueError("End location is not in the graph")

        self._adjacency_list[start][end] = road.travel_time
        self._adjacency_list[end][start] = road.travel_time

    # Get the neighbors of a location along with travel times
    def get_neighbors(self, location: str) -> dict[str, float]:

        # Raise error if location is not in the graph
        if location not in self._adjacency_list:
            raise ValueError("Location is not in the graph")
        
        return self._adjacency_list[location].copy()

    def get_locations(self) -> list[str]:
        return list(self._adjacency_list.keys())