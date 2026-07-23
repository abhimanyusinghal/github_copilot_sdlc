"""Small calculation helpers used in the Copilot lab.

NOTE: these functions intentionally lack input validation and error
handling. You will improve them during the lab (agent mode / review).
"""

from fastmath import mean


def validate_number(value, name):
    """Validate that a value is a real numeric input (int or float, not bool)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be an int or float")
    return value


def safe_divide(numerator, denominator):
    numerator = validate_number(numerator, "numerator")
    denominator = validate_number(denominator, "denominator")
    if denominator == 0:
        raise ValueError("denominator must not be zero")
    return numerator / denominator


def average(numbers):
    if not isinstance(numbers, list):
        raise ValueError("numbers must be a list of numbers")
    if not numbers:
        raise ValueError("numbers must not be empty")
    validated_numbers = [validate_number(n, "numbers[]") for n in numbers]
    return mean(validated_numbers)


def percentage(part, whole):
    part = validate_number(part, "part")
    whole = validate_number(whole, "whole")
    return safe_divide(part, whole) * 100


def apply_discount(price, percent_off):
    price = validate_number(price, "price")
    percent_off = validate_number(percent_off, "percent_off")
    if percent_off < 0 or percent_off > 100:
        raise ValueError("percent_off must be between 0 and 100")
    return price - (price * percent_off / 100)


def median(numbers):
    if not isinstance(numbers, list):
        raise ValueError("numbers must be a list of numbers")
    if not numbers:
        raise ValueError("numbers must not be empty")
    validated_numbers = [validate_number(n, "numbers[]") for n in numbers]

    sorted_numbers = sorted(validated_numbers)
    n = len(sorted_numbers)
    mid = n // 2

    if n % 2 == 1:
        return sorted_numbers[mid]

    return safe_divide(sorted_numbers[mid - 1] + sorted_numbers[mid], 2)
