from utils import fibonacci_series


def test_fibonacci_series_zero():
    assert fibonacci_series(0) == [0]


def test_fibonacci_series_one():
    assert fibonacci_series(1) == [0, 1, 1]


def test_fibonacci_series_ten():
    assert fibonacci_series(10) == [0, 1, 1, 2, 3, 5, 8]


def test_fibonacci_series_stops_before_exceeding_limit():
    assert fibonacci_series(15) == [0, 1, 1, 2, 3, 5, 8, 13]


def test_fibonacci_series_hundred():
    assert fibonacci_series(100) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]


def test_fibonacci_series_negative_input():
    assert fibonacci_series(-1) == []


def test_fibonacci_series_values_do_not_exceed_limit_and_follow_rule():
    limit = 1000
    result = fibonacci_series(limit)

    assert all(value <= limit for value in result)

    for index in range(2, len(result)):
        assert result[index] == result[index - 1] + result[index - 2]