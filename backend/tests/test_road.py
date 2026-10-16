import pytest

from app.road import Road


def test_constructs_road_with_valid_values():
    road = Road("A", "B", 10)

    assert road.start == "A"
    assert road.end == "B"
    assert road.travel_time == 10
    assert road.is_open is True


def test_road_can_be_closed_and_reopened():
    road = Road("A", "B", 10)

    road.close()
    assert road.is_open is False

    road.reopen()
    assert road.is_open is True


def test_updates_travel_time():
    road = Road("A", "B", 10)

    road.update_travel_time(25)

    assert road.travel_time == 25


@pytest.mark.parametrize(
    "start,end,travel_time",
    [
        ("", "B", 10),
        ("A", "", 10),
        ("   ", "B", 10),
        ("A", "   ", 10),
        (None, "B", 10),
        (1, "B", 10),
        ("A", None, 10),
        ("A", 2, 10),
        ("A", "A", 10),
        ("A", "B", -1),
        ("A", "B", "fast"),
        ("A", "B", None),
        ("A", "B", float("inf")),
        ("A", "B", float("-inf")),
        ("A", "B", float("nan")),
        ("A", "B", True),
        ("A", "B", False),
    ],
)
def test_rejects_invalid_constructor_values(start, end, travel_time):
    with pytest.raises((TypeError, ValueError)):
        Road(start, end, travel_time)


@pytest.mark.parametrize("travel_time", [-1, "fast", None, float("inf"), float("-inf"), float("nan"), True, False])
def test_rejects_invalid_updated_travel_time(travel_time):
    road = Road("A", "B", 10)

    with pytest.raises((TypeError, ValueError)):
        road.update_travel_time(travel_time)

    assert road.travel_time == 10

@pytest.mark.parametrize("is_open", ["closed", 1, None])
def test_rejects_invalid_road_status(is_open):
    with pytest.raises((TypeError, ValueError)):
        Road("A", "B", 10, is_open)