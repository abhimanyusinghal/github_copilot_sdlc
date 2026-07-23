# Return the factorial of a non-negative integer n. Raise ValueError if n is negative.
def factorial(n):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result