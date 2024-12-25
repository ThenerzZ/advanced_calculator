def power(base, exponent):
    """Calculate the power of a number."""
    return base ** exponent

def square_root(value):
    """Calculate the square root of a number."""
    if value < 0:
        raise ValueError("Cannot compute square root of a negative number.")
    return value ** 0.5

def logarithm(value, base=10):
    """Calculate the logarithm of a number with a given base."""
    import math
    if value <= 0:
        raise ValueError("Logarithm undefined for non-positive values.")
    return math.log(value, base)