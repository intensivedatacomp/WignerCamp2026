# 📚 NumPy-Style Python Docstrings Guide

This guide explains how to write **NumPy-style docstrings** to document Python code clearly and consistently. It covers parameters, return values, default/optional arguments, examples, equations, and citations.

---

## ✍️ Basic Structure

A NumPy-style docstring typically includes:

- Short summary
- Longer description
- `Parameters` section
- `Returns` section
- Optional `Raises`, `Examples`, `References`

### Example

```python
def function_name(arg1, arg2='foo'):
    """
    Short summary line.

    Extended description that spans multiple lines and explains
    what the function does and why.

    Parameters
    ----------
    arg1 : int
        Description of the first parameter.
    arg2 : str, optional
        Description of the second parameter. Default is 'foo'.

    Returns
    -------
    bool
        True if successful, False otherwise.

    Examples
    --------
    >>> function_name(42)
    True
    """
````

---

## 🧩 Parameters

Each parameter is listed with:

* its name
* its type
* optional status
* default value (in the description)

```python
def compute_area(radius, unit="cm"):
    """
    Compute the area of a circle.

    Parameters
    ----------
    radius : float
        Radius of the circle.
    unit : str, optional
        Measurement unit (e.g., 'cm', 'm'). Default is 'cm'.

    Returns
    -------
    float
        Area of the circle in square units.
    """
```

---

## 🔁 Returns and Yields

For return values:

```python
Returns
-------
area : float
    The computed area.
```

For multiple return values:

```python
Returns
-------
mean : float
    Mean of the values.
std : float
    Standard deviation of the values.
```

---

## ⚠️ Raises

Use this section to document exceptions:

```python
Raises
------
ValueError
    If the input is invalid.
TypeError
    If argument types are incorrect.
```

---

## 💡 Examples

Always provide examples under the `Examples` section using the `>>>` syntax:

```python
Examples
--------
>>> compute_area(1)
3.1416
>>> compute_area(2, unit="m")
12.5664
```

---

## 🧮 Equations with `.. math::`

Use `.. math::` for mathematical expressions in reStructuredText-compatible tools like Sphinx.

```python
"""
Calculate area with the formula:

.. math::

   A = \pi r^2

where :math:`r` is the radius.
"""
```

Use `:math:` inline inside text for simple math expressions.

---

## 📖 Citing Sources

Use a `References` section to cite works:

```python
"""
Implements the algorithm described in [1].

References
----------
[1] Turing, A. (1936). On Computable Numbers, with an Application to the Entscheidungsproblem.
"""
```

---

## 🧱 Documenting Classes

```python
class Circle:
    """
    A class representing a circle.

    Attributes
    ----------
    radius : float
        Radius of the circle.

    Methods
    -------
    area()
        Return the area.
    perimeter()
        Return the perimeter.
    """

    def __init__(self, radius):
        """
        Initialize the circle.

        Parameters
        ----------
        radius : float
            The radius of the circle.
        """
        self.radius = radius

    def area(self):
        """
        Return the area.

        Returns
        -------
        float
            The area computed as:

            .. math::

               A = \pi r^2
        """
        return 3.1416 * self.radius**2
```

---

## ✅ Best Practices

* One-line summary followed by an empty line
* Use `optional` keyword for optional arguments
* Align types and colons for clarity
* Wrap lines at \~80 characters
* Include doctest-style examples where appropriate

---

## 🛠️ Tools Supporting This Style

* [Sphinx](https://www.sphinx-doc.org) with `napoleon` extension
* [pdoc](https://pdoc.dev)
* `doctest` from Python standard library
* IDEs like PyCharm and VS Code (with plugins)

---

## 📚 Additional Resources

* [NumPy Docstring Standard](https://numpydoc.readthedocs.io/en/latest/format.html)
* [PEP 257](https://peps.python.org/pep-0257/)
* [Sphinx Napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
