import math

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
    if value <= 0:
        raise ValueError("Logarithm undefined for non-positive values.")
    return math.log(value, base)

def sin(angle, is_radians=True):
    """Calculate sine of an angle."""
    if not is_radians:
        angle = math.radians(angle)
    return math.sin(angle)

def cos(angle, is_radians=True):
    """Calculate cosine of an angle."""
    if not is_radians:
        angle = math.radians(angle)
    return math.cos(angle)

def tan(angle, is_radians=True):
    """Calculate tangent of an angle."""
    if not is_radians:
        angle = math.radians(angle)
    return math.tan(angle)

def factorial(n):
    """Calculate factorial of a number."""
    if not isinstance(n, int) or n < 0:
        raise ValueError("Factorial is only defined for non-negative integers.")
    return math.factorial(n)

def exp(x):
    """Calculate e raised to the power of x."""
    return math.exp(x)

def pi():
    """Return the value of π (pi)."""
    return math.pi

def e():
    """Return the value of e (Euler's number)."""
    return math.e