import pytest

from src.calculations import (
    apply_discount,
    average,
    median,
    percentage,
    safe_divide,
    validate_number,
)


def test_average_basic():
    assert average([2, 4, 6]) == 4


def test_percentage_basic():
    assert percentage(25, 100) == 25


def test_safe_divide_basic():
    assert safe_divide(9, 3) == 3


def test_safe_divide_rejects_zero_denominator():
    with pytest.raises(ValueError, match="denominator must not be zero"):
        safe_divide(1, 0)


def test_average_rejects_empty_list():
    with pytest.raises(ValueError, match="numbers must not be empty"):
        average([])


def test_percentage_rejects_zero_whole():
    with pytest.raises(ValueError, match="denominator must not be zero"):
        percentage(25, 0)


def test_apply_discount_rejects_out_of_range_percentage():
    with pytest.raises(ValueError, match="percent_off must be between 0 and 100"):
        apply_discount(100, 150)


def test_validate_number_accepts_int_and_float():
    assert validate_number(5, "value") == 5
    assert validate_number(2.5, "value") == 2.5


def test_validate_number_rejects_non_numeric_value():
    with pytest.raises(ValueError, match="value must be an int or float"):
        validate_number("5", "value")


def test_validate_number_rejects_bool():
    with pytest.raises(ValueError, match="value must be an int or float"):
        validate_number(True, "value")


def test_median_odd_count():
    assert median([3, 1, 2]) == 2


def test_median_even_count():
    assert median([1, 2, 3, 4]) == 2.5


def test_median_rejects_empty_list():
    with pytest.raises(ValueError, match="numbers must not be empty"):
        median([])


def test_median_rejects_non_list_input():
    with pytest.raises(ValueError, match="numbers must be a list of numbers"):
        median((1, 2, 3))


def test_median_rejects_non_numeric_values():
    with pytest.raises(ValueError, match="numbers\[\] must be an int or float"):
        median([1, "2", 3])