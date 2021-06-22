import re

import numpy as np


def is_close(a, b):
    return abs(a - b) < 1e-4


def solve_sum_min(eq, val):
    """Solve a sum of min equations numerically.

    Args:
        eq: string of min equation
        val: float, the value to solve on the RHS
        var: str, the name of the variable
    >>> equation = 'min(400, 400*a) + min(400, 400*a) + min(0, 100*a)'
    >>> value = 200
    >>> solve_sum_min(equation, value)
    0.25
    """
    # TODO: representation, a or x
    # TODO: alpha range
    # TODO: no solution
    p = re.compile("\d+")
    alpha = np.arange(0, 1, 0.001)
    min_sum = np.zeros(len(alpha))
    for min_eq in eq.split("+"):
        params = p.findall(min_eq)
        val_array = np.repeat(float(params[0]), len(alpha))
        min_sum += np.minimum(val_array, float(params[1])*alpha)
    for i, v in enumerate(min_sum):
        if is_close(v, val):
            return alpha[i]
    print("No solution found!")


def solve_sum_max(eq, val):
    """Solve a sum of min equations numerically.

        Args:
            eq: string of min equation
            val: the value to solve on the RHS
        >>> equation = 'max(40, 50*a) + max(40, 50*a)'
        >>> value = 60
        >>> solve_sum_max(equation, value)
        No solution found!
        """
    # TODO: representation, a or x
    p = re.compile("\d+")
    alpha = np.arange(0, 1, 0.001)
    max_sum = np.zeros(len(alpha))
    for max_eq in eq.split("+"):
        params = p.findall(max_eq)
        val_array = np.repeat(float(params[0]), len(alpha))
        max_sum += np.maximum(val_array, float(params[1]) * alpha)
    for i, v in enumerate(max_sum):
        if is_close(v, val):
            return alpha[i]
    print("No solution found!")


if __name__ == "__main__":
    import doctest
    doctest.testmod()

