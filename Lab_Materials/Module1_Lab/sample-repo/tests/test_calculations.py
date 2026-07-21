from src.calculations import average, percentage, apply_discount


def test_average_basic():
    assert average([2, 4, 6]) == 4


def test_percentage_basic():
    assert percentage(25, 100) == 25


# TODO (lab): add edge-case tests - empty list, whole == 0,
# and percent_off outside 0-100. Try asking Copilot: /tests
