import re
import numpy as np
# TODO: what if the user enters multiple variables
# TODO: user enters a fraction


def convert_letters(matchobj):
    m = matchobj.group()
    match_map = {m: "*alpha"} if len(m) == 2 else {m: m}
    return match_map[m]


def convert_digits(matchobj):
    m = matchobj.group()
    match_map = {m: f"np.repeat({m}, len(alpha))"}
    return match_map[m]


def knit_str(equation):
    eq_replaced = re.sub(r"\*([a-z]+)", convert_letters, equation)
    eq_replaced = re.sub(r"\d+", convert_digits, eq_replaced)
    eq_replaced = (eq_replaced.replace("min", "np.minimum")
                   .replace("max", "np.maximum"))
    return eq_replaced


def solve_sum_minmax(equation, val, low=0, high=1.0, acc=5):
    """Solve a sum of min equations numerically.

    Args:
        equation: string of min equation
        val: float, the value to solve on the RHS
        low: float, the lower bound of the variable
        high: float, the higher bound of the variable
        acc: int, the magnitude of accuracy
    """
    alpha = np.arange(low, high, 10**(-acc))
    eq_sum = np.zeros(len(alpha))
    eq_replaced = knit_str(equation)
    eq_sum += eval(eq_replaced)
    for i, v in enumerate(eq_sum):
        if np.isclose(v, val):
            return alpha[i]
    print("No solution found!")


if __name__ == "__main__":
    eq = "min(500, 600*a) + max(400, 500*a)"
    value = 500
    solve_sum_minmax(eq, value)
