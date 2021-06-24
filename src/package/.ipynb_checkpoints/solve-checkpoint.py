import re
from sympy import N
from sympy.solvers import solve
from sympy import Symbol
from itertools import product


def convert_letters(matchobj):
    m = matchobj.group()
    match_map = {m: "*result[0]"} if len(m) == 2 else {m: m}
    return match_map[m]


# def knit_str(equation):
#     eq_replaced = re.sub(r"\*([a-z]+)", convert_letters, equation)
#     eq_replaced = re.sub(r"\d+", convert_digits, eq_replaced)
#     eq_replaced = (eq_replaced.replace("min", "np.minimum")
#                    .replace("max", "np.maximum"))
#     return eq_replaced
#
#
# def extract_eq_val(equation_str):
#     m = re.search(r"([^=]+)=\s+(\d+)", equation_str)
#     if m:
#         return m.group(1), float(m.group(2))


def solve_sum_minmax(equation, low=0, high=1.0, float=False):
    """Solve a sum of min equations numerically.

    Args:
        equation: string of min equation
        low: float, the lower bound of the variable, exclusive
        high: float, the higher bound of the variable, exclusive
        float: bool,whether to return exact float value
    """
    equation = f"+{equation}"
    value = re.search(r"=\s*(\d+)", equation).group(1)
    compartments = re.findall(r"(\+|\-)\s*(min|max)(\([^\)]+\))", equation)

    lists = []
    for part in compartments:
        match = re.match(r"(\d+[\*a-z]*),\s+(\d+[\*a-z]*)", part[2])
        lists.append([match.group(1), match.group(2)])
    products = list(product(*lists))

    a_replace = re.sub(r"\*([a-z]+)", convert_letters, equation)
    a_replace = a_replace.replace(r"=", "==")
    a = Symbol("a")

    for p in products:
        knit = ""
        for i, operand in enumerate(p):
            operator = compartments[i][0]
            knit += f"{operator}{operand}"
        knit += f"-{value}"
        result = solve(eval(knit), a)
        if len(result) == 0:
            continue
        elif (result[0] <= low) or (result[0]) >= high:
            continue
        if eval(a_replace):
            if float:
                return N(result[0])
            else:
                return result[0]
    return None


if __name__ == "__main__":
    eq = "min(400, 400*a) + min(400, 400*a) + min(0, 100*a) = 200"
    solve_sum_minmax(eq)
