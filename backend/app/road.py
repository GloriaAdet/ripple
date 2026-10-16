# Road class
class Road:
    def __init__(self, start: str, end: str, travel_time: float, is_open: bool = True):

        # Validate input, travel time cannot be negative, and is finite
        if not isinstance(travel_time, (int, float)) or travel_time < 0 or not float('-inf') < travel_time < float('inf'):
            raise ValueError("Travel time must be a finite, nonnegative number")

        # Validate is_open is a boolean
        if not isinstance(is_open, bool):
            raise ValueError("is_open must be a boolean value")

        # Validate start and end are non-empty strings and not the same
        if not isinstance(start, str) or not start.strip():
            raise ValueError("Start must be a non-empty location name")
        if not isinstance(end, str) or not end.strip():
            raise ValueError("End must be a non-empty location name")
        if start == end:
            raise ValueError("A road cannot connect a location to itself")

        # Validate that travel_time is not a boolean
        if isinstance(travel_time, bool):
            raise ValueError("Travel time must be a finite, nonnegative number")

        self._start = start
        self._end = end
        self._travel_time = travel_time
        self._is_open = is_open

    # close the road
    def close(self):
        self._is_open = False

    # reopen the road
    def reopen(self):
        self._is_open = True

    # update the travel time of the road, should not be a negative number and should be finite and not a boolean    
    def update_travel_time(self, value: float):   
        if not isinstance(value, (int, float)) or value < 0 or not float('-inf') < value < float('inf'):
            raise ValueError("Travel time must be a finite, nonnegative number")
        if isinstance(value, bool):
            raise ValueError("Travel time must be a finite, nonnegative number")
        
        self._travel_time = value

    # Getters
    @property
    def travel_time(self) -> float:
        return self._travel_time

    @property
    def is_open(self) -> bool:
        return self._is_open

    @property
    def start(self) -> str:
        return self._start

    @property
    def end(self) -> str:
        return self._end
