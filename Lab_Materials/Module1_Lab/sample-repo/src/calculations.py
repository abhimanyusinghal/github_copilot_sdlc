"""Small calculation helpers used in the Copilot lab.

NOTE: these functions intentionally lack input validation and error
handling. You will improve them during the lab (agent mode / review).
"""


def average(numbers):
    # Bug: crashes on an empty list (ZeroDivisionError)
    return sum(numbers) / len(numbers)


def percentage(part, whole):
    # Bug: crashes when whole == 0
    return (part / whole) * 100


def apply_discount(price, percent_off):
    # Bug: allows percent_off > 100 (negative price) or < 0
    return price - (price * percent_off / 100)
