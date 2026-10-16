import pytest

from app.graph import Graph
from app.road import Road


def test_add_location():
    graph = Graph()
    graph.add_location("A")

    assert graph.get_neighbors("A") == {}


def test_add_duplicate_location_preserves_roads():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_road("A", "B", 10.0)

    graph.add_location("A")

    assert graph.get_neighbors("A")["B"].travel_time == 10.0
    assert graph.get_neighbors("B")["A"].travel_time == 10.0


def test_add_bidirectional_road():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")

    graph.add_road("A", "B", 10.0)

    road_from_a = graph.get_neighbors("A")["B"]
    road_from_b = graph.get_neighbors("B")["A"]

    assert isinstance(road_from_a, Road)
    assert road_from_a is road_from_b
    assert road_from_a.start == "A"
    assert road_from_a.end == "B"
    assert road_from_a.travel_time == 10.0


def test_update_road():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_road("A", "B", 10.0)

    graph.add_road("A", "B", 15.0)

    assert graph.get_neighbors("A")["B"].travel_time == 15.0
    assert graph.get_neighbors("B")["A"].travel_time == 15.0

    with pytest.raises(ValueError):
        graph.add_road("A", "Z", 3.0)


@pytest.mark.parametrize(
    "travel_time",
    [-5.0, float("inf"), float("-inf"), float("nan"), "fast", None, True, False],
)
def test_rejects_invalid_travel_time_without_changing_graph(travel_time):
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_road("A", "B", 4.0)

    with pytest.raises((TypeError, ValueError)):
        graph.add_road("A", "B", travel_time)

    assert graph.get_neighbors("A")["B"].travel_time == 4.0
    assert graph.get_neighbors("B")["A"].travel_time == 4.0


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

    with pytest.raises(ValueError):
        graph.add_road("A", "Z", 5.0)

    with pytest.raises(ValueError):
        graph.add_road("Z", "A", 5.0)

    with pytest.raises(ValueError):
        graph.get_neighbors("Z")

    assert graph.get_neighbors("A") == {}


def test_returned_neighbors_do_not_expose_internal_dictionary():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_road("A", "B", 10.0)

    neighbors = graph.get_neighbors("A")
    neighbors.clear()

    assert graph.get_neighbors("A")["B"].travel_time == 10.0
    assert graph.get_neighbors("B")["A"].travel_time == 10.0


def test_zero_travel_time():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")

    graph.add_road("A", "B", 0.0)

    assert graph.get_neighbors("A")["B"].travel_time == 0.0
    assert graph.get_neighbors("B")["A"].travel_time == 0.0


def test_get_locations_returns_a_copy():
    graph = Graph()
    graph.add_location("A")

    locations = graph.get_locations()
    locations.append("B")

    assert graph.get_locations() == ["A"]

def test_close_road():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")

    # Check if the road is non existent before adding it
    with pytest.raises(ValueError):
        graph.close_road("A", "B")

    graph.add_road("A", "B", 10.0)

    # Close the road between A and B
    graph.close_road("A", "B")

    # Check that the road is closed
    assert not graph.get_neighbors("A")["B"].is_open
    assert not graph.get_neighbors("B")["A"].is_open

    # Check that closing the road again does not raise an error
    graph.close_road("A", "B")
    assert graph.get_neighbors("A")["B"].is_open is False

def test_reopen_road():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")

    # Check if the road is non existent before adding it
    with pytest.raises(ValueError):
        graph.reopen_road("A", "B")

    graph.add_road("A", "B", 10.0)

    # Close the road between A and B
    graph.close_road("A", "B")

    # Reopen the road between A and B
    graph.reopen_road("A", "B")

    # Check that the road is open
    assert graph.get_neighbors("A")["B"].is_open
    assert graph.get_neighbors("B")["A"].is_open

    # Check that reopening the road again does not raise an error
    graph.reopen_road("A", "B")
    assert graph.get_neighbors("A")["B"].is_open is True

def test_add_road_replaces_existing_road():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_road("A", "B", 10.0)
    original_road = graph.get_neighbors("A")["B"]

    graph.add_road("A", "B", 15.0)

    replacement_road = graph.get_neighbors("A")["B"]
    assert replacement_road.travel_time == 15.0
    assert replacement_road is not original_road
    assert graph.get_neighbors("B")["A"] is replacement_road


@pytest.mark.parametrize("is_open", [True, False])
def test_update_road_changes_travel_time_and_preserves_road(is_open):
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_road("A", "B", 10.0)

    road = graph.get_neighbors("A")["B"]
    if not is_open:
        graph.close_road("A", "B")

    graph.update_road("A", "B", 15.0)

    assert road.travel_time == 15.0
    assert road.is_open is is_open
    assert graph.get_neighbors("A")["B"] is road
    assert graph.get_neighbors("B")["A"] is road


@pytest.mark.parametrize(
    "travel_time",
    [-1, "fast", None, float("inf"), float("-inf"), float("nan"), True, False],
)
def test_update_road_rejects_invalid_travel_time_without_changing_road(travel_time):
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")
    graph.add_road("A", "B", 10.0)
    road = graph.get_neighbors("A")["B"]

    with pytest.raises((TypeError, ValueError)):
        graph.update_road("A", "B", travel_time)

    assert road.travel_time == 10.0
    assert graph.get_neighbors("A")["B"] is road
    assert graph.get_neighbors("B")["A"] is road


def test_update_road_raises_for_nonexistent_road():
    graph = Graph()
    graph.add_location("A")
    graph.add_location("B")

    with pytest.raises(ValueError):
        graph.update_road("A", "B", 15.0)