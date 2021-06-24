import re
from sympy import N
from sympy.solvers import solve
from sympy import Symbol
from itertools import product
# TODO: what if the solution is a range?


def convert_letters(matchobj):
    m = matchobj.group()
    match_map = {m: "*result[0]"} if len(m) == 2 else {m: m}
    return match_map[m]


def solve_sum_minmax(equation, var_name, low=0, high=1.0, decimal=False):
    """Solve a sum of min equations numerically.

    Args:
        equation: string of min equation
        var_name: char, the variable
        low: float, the lower bound of the variable, exclusive
        high: float, the higher bound of the variable, exclusive
        decimal: bool,whether to return exact float value
    """
    equation = f"+{equation}"
    value = re.search(r"=\s*(\d+)", equation).group(1)
    minmax_parts = re.findall(r"(\+|\-)\s*(min|max)(\([^\)]+\))", equation)
    digit_parts = re.findall(r"((\+|\-)\s*\d+(\*[a-z])+)", equation)

    lists = []
    for e in minmax_parts:
        match = re.findall(r"(\d+[\*a-z]*),\s+(\d+[\*a-z]*)", e[2])
        lists.append(match[0])
    products = product(*lists)

    a_replace = re.sub(r"\*([a-z]+)", convert_letters, equation)
    a_replace = a_replace.replace(r"=", "==")
    x = var_name
    exec(f"x = {Symbol(x)}")
    print(var_name)
    return

    for p in products:
        knit = ""
        for digit_part in digit_parts:
            knit += digit_part[0]
        for i, operand in enumerate(p):
            operator = minmax_parts[i][0]
            knit += f"{operator}{operand}"
        knit += f"-{value}"
        result = solve(eval(knit), a)
        if len(result) == 0:
            continue
        elif (result[0] <= low) or (result[0]) >= high:
            continue
        if eval(a_replace):
            if decimal:
                return N(result[0])
            else:
                return result[0]
    return None


if __name__ == "__main__":
    eq = "min(500, 600*a) - min(500, 600*a) = 0"
    print(solve_sum_minmax(eq, "a"))
