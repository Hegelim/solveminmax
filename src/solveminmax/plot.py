from src.solveminmax import solver
import matplotlib.pyplot as plt
import numpy as np


def make_plot(equation, low=0, high=1):
    """Plot the equation.

    Args:
        equation (str): The string of the equation.
        low (float): The lower bound of the variable.
        high (float): The upper bound of the variable.

    Returns:
        None

    """
    lhs = solver.get_lhs(equation)
    value = solver.get_value_term(equation)
    replaced = lhs.replace("min", "np.minimum").replace("max", "np.maximum")
    replaced = f"{replaced} - {value}"
    minmax_terms = solver.get_minmax_terms(equation)
    set_points = solver.find_set_points(minmax_terms, "a")
    """Now the default variable is still a. """
    a = np.arange(low, high, 0.001)
    y = eval(replaced)
    plt.plot(a, y)
    for pt in set_points:
        plt.axvline(pt, linestyle="--", color="orange")
    plt.axhline(0, linestyle="--", color="brown")
    plt.title(equation)
    plt.show()
