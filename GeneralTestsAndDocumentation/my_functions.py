import numpy as np
import math

def square(x):
    """
    Return the square of a number.

    Parameters
    ----------
    x : float or int
        Input number.

    Returns
    -------
    float or int
        The square of the input.
    """
    return x * x

def divide(x, y):
    """
    Divide two numbers.

    Parameters
    ----------
    x : float
        Numerator.
    y : float
        Denominator.

    Returns
    -------
    float
        Result of the division.

    Raises
    ------
    ZeroDivisionError
        If y is zero.
    """
    return x / y

def reciprocal(x):
    """
    Return the reciprocal of a number.

    Parameters
    ----------
    x : float
        Input value.

    Returns
    -------
    float
        Reciprocal of x.

    Raises
    ------
    ZeroDivisionError
        If x is zero.
    """
    return 1 / x

def normalize(v):
    """
    Normalize a vector to have unit norm.

    Parameters
    ----------
    v : ndarray
        Input NumPy vector.

    Returns
    -------
    ndarray
        Normalized vector (unit norm).
    """
    return v / np.linalg.norm(v)

def double(x):
    """
    Double the input value.

    Parameters
    ----------
    x : float or int
        Input value.

    Returns
    -------
    float or int
        Twice the input value.
    """
    return 2 * x

def safe_log(x):
    """
    Return the natural logarithm of x if x > 0.

    Parameters
    ----------
    x : float
        Input value.

    Returns
    -------
    float
        Natural logarithm of x.

    Raises
    ------
    ValueError
        If x is not positive.
    """
    if x <= 0:
        raise ValueError("x must be positive")
    return math.log(x)