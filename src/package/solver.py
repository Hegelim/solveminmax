import re
from sympy import N, FiniteSet, Symbol, EmptySet, Complexes
from sympy.solvers import solveset
from itertools import product
# TODO: what if the solution is a range?
# TODO: what if the equation starts with a -?
# TODO: what if the interval is open on one end
# TODO: what if the interval is infinity on one end?
# TODO: what if there are two numbers inside the min?


def get_value_term(equation):
    return re.search(r"=\s*(\d+)", equation).group(1)


def get_minmax_terms(equation):
    """Return a list of tuples. """
    return re.findall(r"(\+|\-)\s*(\d*)\s*\**\s*(min|max)(\([^\)]+\))",
                      equation)


def get_cons_var_terms(equation):
    return re.findall(r"(\+|\-)\s*(\d+)\s*\*\s*([a-z]+)", equation)


def gen_combs(minmax_terms):
    """Return itertools.product object. """
    lists = []
    for e in minmax_terms:
        match = re.findall(r"(\d+[\*a-z]*),\s*(\d+[\*a-z]*)", e[3])
        lists.append(match[0])
    return product(*lists)


def gen_validate_eq(equation):
    return (re.sub(r"\*([a-z]+)", convert_letters, equation)
            .replace(r"=", "=="))


def convert_letters(matchobj):
    m = matchobj.group()
    match_map = {m: "*next(iter(result))"} if len(m) == 2 else {m: m}
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
    # TODO: if the equation starts with a -
    equation = f"+{equation}"
    value_term = get_value_term(equation)
    minmax_terms = get_minmax_terms(equation)
    cons_var_terms = get_cons_var_terms(equation)
    products = gen_combs(minmax_terms)
    validate_eq = gen_validate_eq(equation)
    x = Symbol("x")

    for p in products:
        knitted = ""
        for digit_part in cons_var_terms:
            knitted += digit_part[0]
        for i, operand in enumerate(p):
            count = int(minmax_terms[i][1]) if minmax_terms[i][1] != "" else 1
            for j in range(count):
                operator = minmax_terms[i][0]
                knitted += f"{operator}{operand}"
        knitted += f"-{value_term}"
        knitted = knitted.replace(var_name, "x")
        result = solveset(eval(knitted), x)
        if result == EmptySet:
            continue
        elif result == Complexes:
            continue
        elif result == FiniteSet and \
                (next(iter(result)) <= low) or (next(iter(result)) >= high):
            continue
        if eval(validate_eq):
            if decimal:
                return N(next(iter(result)))
            else:
                return next(iter(result))
    return None


if __name__ == "__main__":
    eq = "min(300, 400*a) = 300"
    print(solve_sum_minmax(eq, "a"))
