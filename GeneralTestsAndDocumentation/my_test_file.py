import pytest
import numpy as np
import math
from my_functions import *

def test_square():
    """
    Test the square function.

    Asserts that squaring positive and negative integers returns the correct result.
    """
    assert square(2) == 4
    assert square(-3) == 9

def test_divide_by_zero():
    """
    Test that dividing by zero raises ZeroDivisionError.

    Uses pytest.raises to ensure the exception is correctly raised.
    """
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

def test_reciprocal():
    """
    Test the reciprocal function for correctness with floating point values.

    Asserts that the result is approximately equal to the expected value using pytest.approx.
    """
    assert reciprocal(2.0) == pytest.approx(0.5)

def test_normalize():
    """
    Test the normalize function with a simple vector.

    Asserts that the result is close to the expected normalized vector using np.testing.assert_allclose.
    """
    v = np.array([3.0, 4.0])
    expected = np.array([0.6, 0.8])
    np.testing.assert_allclose(normalize(v), expected, rtol=1e-5)

def test_fail():
    """
    Demonstrates a failing test for illustration purposes.

    This test always fails to show how pytest reports failures.
    """
    assert (1 + 1) == 3

def test_double():
    """
    TODO: write docstring here.
    """
    # TODO: write your solution here
    pass

def test_safe_log():
    """
    TODO: write docstring here
    """
    # TODO: write your solution here
    pass
