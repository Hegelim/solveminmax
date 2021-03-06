import re
from sympy import S, Symbol, EmptySet, Interval, FiniteSet
from sympy.solvers import solveset
import numpy as np
from src.solveminmax.minmax_term import MinMaxTerm
from src.solveminmax.cons_var_term import ConsVarTerm
# TODO: what if the equation starts with a -?
# TODO: what if the interval is infinity on one end?


def get_lhs(equation: str) -> str:
    """Get the left-hand side of the equation.

    Args:
        equation: The string of the equation to be solved.

    Returns:
        A string of the left-hand side of the equation.

    """
    index = equation.find("=")
    return equation[:index]


def get_constants(equation):
    """Extract constants from the left-hand side of the equation.

    Args:
        equation (str): A string of the equation to be solved.

    Returns:
        str: A list of constants on the LHS of the equation.

    """
    lhs = get_lhs(equation)
    l = []
    for t in lhs.split():
        try:
            l.append(float(t))
        except ValueError:
            pass
    return l


def get_minmax_terms(equation):
    """Get a list of minmax terms.

    Args:
        equation (str): A string of the equation to be solved.

    Returns:
        list: A list of minmax_term objects.

    """
    minmax_terms = re.findall(r"([\+\-])\s*(\d*)\s*\**\s*(min|max)"
                              r"(\([^\)]+\))", equation)
    minmax_objects = []
    for term in minmax_terms:
        minmax_objects.append(MinMaxTerm(term))
    return minmax_objects


def get_cons_var_terms(equation):
    """Get a list of cons_var_terms.

    Args:
        equation (str): A string of the equation to be solved.

    Returns:
        list: A list of cons_var_term objects.

    """
    match_list = re.findall(r"(\+|\-)\s*(\d+)\s*\*\s*([a-z]+)", equation)
    i = 0
    n = len(match_list)
    while i < len(match_list):
        if "min" in match_list[i][2] or "max" in match_list[i][2]:
            match_list.pop(i)
            i -= 1
            n -= 1
        i += 1
    cons_var_objects = []
    for term in match_list:
        cons_var_objects.append(ConsVarTerm(term))
    return cons_var_objects


def find_set_points(minmax_terms, var_name):
    """Return a list of sorted set points.

    Args:
        minmax_terms (list): A list of minmax_term objects.
        var_name (str): A character, which is the name of the variable.

    Returns:
        list: An empty list if there are variables but all coefficients are 0,
        such as min(30, 0*a), or if there are simply no variables, such as
        min(30, 30).

    """
    pts = set()
    for term in minmax_terms:
        left, right = term.left_right_nums()
        left_half, right_half = term.left_right_half()
        if var_name in left_half:
            try:
                pts.add(right / left)
            except ZeroDivisionError:
                continue
        elif var_name in right_half:
            try:
                pts.add(left / right)
            except ZeroDivisionError:
                continue
    return sorted(pts)


def create_intervals(set_points, low=0, high=1, left_open=True,
                     right_open=True):
    """Create a list of intervals based on set_points.

    Args:
        set_points (list): A list of sorted set points.
        low (float): The lower bound of the variable.
        high (float): The higher bound of the variable.
        left_open (bool): True if the bound is open on the left.
        right_open (bool): True if the bound is open on the right.

    Returns:
        list: A list of Interval objects based on set points.

    """
    intervals = []
    i = -1
    j = 0
    while i < len(set_points):
        if i == -1:
            interval = Interval(low, set_points[j],
                                left_open=left_open, right_open=True)
            if interval is not EmptySet:
                intervals.append(interval)
        elif j == len(set_points):
            interval = Interval(set_points[i], high,
                                left_open=True, right_open=right_open)
            if interval is not EmptySet:
                intervals.append(interval)
        else:
            intervals.append(Interval(set_points[i], set_points[j],
                                      left_open=True, right_open=True))
        i += 1
        j += 1
    return intervals


def get_validate_eq(equation):
    """Return a modified equation string with = replaced by ==.

    Args:
        equation (str): The equation to be solved.

    Returns:
        str: A modified equation string with = replaced by ==.

    """
    return equation.replace("=", "==")


def random_interval(interval):
    """Generate a random number in the interval.

    Args:
        interval (:object:Interval): An Interval object.

    Returns:
        float: A random number generated uniformly from the interval.

    """
    return np.random.uniform(interval.start, interval.end)


def get_value_term(equation):
    """Get the value term on the right hand side of the equation.

    Args:
        equation (str): The equation to be solved.

    Returns:
        str: The value term as a string.

    """
    return re.findall(r"=\s*(.*\d+)", equation)[0]


def knit_solver(interval, minmax_terms, cons_var_terms, var_name):
    """Generate a string to be fed into the solver.

    Args:
        interval (:object:Interval): An Interval object.
        minmax_terms (list): A list of minmax_term objects.
        cons_var_terms (list): A list of cons_var_term objects.
        var_name (str): The character of the variable.

    Returns:
        str: A knitted string of the equation.

    """
    solver = ""
    for term in minmax_terms:
        if var_name not in term.minmax_tuple():
            val = eval(f"{term.minmax_op()}{term.minmax_tuple()}")
            solver += f"{term.operator()}{term.coef()}*{val}"
        else:
            rand = random_interval(interval)
            index = term.minmax_tuple().rfind(var_name)
            replaced = (term.minmax_tuple()[:index]
                        + "rand" + term.minmax_tuple()[index + 1:])
            replaced = f"{term.minmax_op()}{replaced}"
            left, right = term.left_right_half()
            if var_name not in left:
                non_var_part = left
                var_part = right
            else:
                non_var_part = right
                var_part = left
            try:
                val = eval(replaced)
            except Exception as e:
                print(e)
                return
            if val != float(non_var_part):
                solver += f"{term.operator()}{term.coef()}*{var_part}"
            else:
                solver += f"{term.operator()}{term.coef()}*{non_var_part}"
    for term in cons_var_terms:
        solver += f"{term.operator()}{term.coef()}*{term.var()}"
    return solver


def reformat_and_solve(knit, value_term):
    """Reformat the knit str then solve with solveset.

    Args:
        knit (str): The knitted equation string.
        value_term (str): The value term of the equation.

    Returns:
        Solution after being solved by solveset.

    """
    s = f"{knit} - {value_term}"
    a = Symbol("a")
    return solveset(eval(s), a)


def solve_linear_eq(cons_var_terms, value_term, low, high,
                    left_open, right_open):
    """Solve a linear equation if the equation does not contain minmax_terms.

    Args:
        cons_var_terms (list): A list of cons_var_term objects.
        value_term (str): The value term of the equation.
        low (float): The lower bound of the variable.
        high (float): The upper bound of the variable.
        left_open (bool): True if the bound is open on the left.
        right_open (bool): True if the bound is open on the right.

    Returns:
        Solution after being solved by solveset.

    """
    knit = ""
    for term in cons_var_terms:
        knit += f"{term.operator()}{term.coef()}*{term.var()}"
    result = reformat_and_solve(knit, value_term)
    if result is S.Complexes:
        return result.intersect(Interval(low, high, left_open=left_open,
                                         right_open=right_open))
    else:
        return result


def extract_val_from_str(s):
    """Extract value from string.

    Args:
        s (str): A string that looks like "200*a"

    Returns:
        float: The float from the string.

    """
    index = s.find("*")
    return float(s[:index])


def minmax_replace_zeros(minmax_terms):
    """Replace zero coefficients minmax_terms with reformatted minmax_terms.

    Args:
        minmax_terms (list): A list of minmax_term objects.

    Returns:
        None

    """
    i = 0
    n = len(minmax_terms)
    while i < n:
        term = minmax_terms[i]
        left, right = term.left_right_half()
        if "a" in left and "*" in left:
            num = extract_val_from_str(left)
            non_var_term = right
        elif "a" in right and "*" in right:
            num = extract_val_from_str(right)
            non_var_term = left
        else:
            # If the term does not contain variables.
            i += 1
            continue
        if num == 0:
            minmax_terms[i] = MinMaxTerm((term.operator(), term.coef(),
                                          term.minmax_op(),
                                          f"(0,{non_var_term})"))
        i += 1


def solve_no_minmax_var(minmax_terms, cons_var_terms, value_term):
    """Solve the equation when there are no variables in minmax_terms.

    For example, when minmax_terms look like min(30, 30) or min(30, 0*a).

    Args:
        minmax_terms (list): A list of minmax_term objects.
        cons_var_terms (list): A list of cons_var_term objects.
        value_term (str): The value term.

    Returns:
        Solution returned by solveset.

    """
    knit = ""
    for term in minmax_terms:
        knit += f"{term.operator()}{term.coef()}*" \
                f"{term.minmax_op()}{term.minmax_tuple()}"
    for term in cons_var_terms:
        knit += f"{term.operator()}{term.coef()}*{term.var()}"
    return reformat_and_solve(knit, value_term)


def get_next(result):
    """Get next item in the result set.

    Args:
        result (:object:FiniteSet): The result returned by solveset.

    Returns:
        The next item in result.

    """
    return next(iter(result))


def get_next_eval(result):
    """Return the evaluate next item from result.

    Args:
        result (:object:FiniteSet): The result returned by solveset.

    Returns:
        The next item in result, evaluated by calling .evalf().

    """
    return get_next(result).evalf()


def find_intersect(interval, low, high, left_open, right_open):
    """Return the intersect of the interval with the required interval
    specified by low, high, left_open, and right_open.

    Args:
        interval (:object:Interval): An Interval object.
        low (float): The lower bound of the variable.
        high (float): The upper bound of the variable.
        left_open (bool): True if the bound is open on the left.
        right_open (bool): True if the bound is open on the right.

    Returns:
        :object:Interval: The intersection of the interval with required
        interval.

    """
    return interval.intersect(Interval(low, high, left_open, right_open))


def append_interval_complexes(interval, eq, low, high, results):
    """Handle the case when the result is S.Complexes.

    Args:
        interval (:object:Interval): An Interval object.
        eq (str): The equation to be solved.
        low (float): The lower bound of the variable.
        high (float): The upper bound of the variable.
        results (list): The list of final results.

    Returns:
        None

    """
    temp_interval = interval
    validate_eq = get_validate_eq(eq)
    a = interval.start
    if a != low and eval(validate_eq):
        temp_interval = temp_interval.union(FiniteSet(a))
    a = interval.end
    if a != high and eval(validate_eq):
        temp_interval = temp_interval.union(FiniteSet(a))
    results.append(temp_interval)


def append_interval_endpoints(interval, eq, result, results, low, high):
    """Handle the cases when result is interval.start or is interval.end.

    Args:
        interval (:object:Interval): An Interval object.
        eq (str): The equation to be solved.
        result (:object:FiniteSet): The current result as FiniteSet object.
        results (list): The list of final results.
        low (float): The lower bound of the variable.
        high (float): The upper bound of the variable.

    Returns:
        None

    """
    a = random_interval(interval)
    if get_next_eval(result) == interval.start:
        validate_eq = get_validate_eq(eq)
        if eval(validate_eq):
            temp_interval = interval.union(result)
            a = interval.end
            if a == high:
                results.append(temp_interval)
            elif eval(validate_eq):
                results.append(temp_interval.union(FiniteSet(a)))
            else:
                results.append(temp_interval)
    else:
        validate_eq = get_validate_eq(eq)
        if eval(validate_eq):
            temp_interval = interval.union(result)
            a = Interval.start
            if a == low:
                results.append(temp_interval)
            elif eval(validate_eq):
                results.append(temp_interval.union(FiniteSet(a)))
            else:
                results.append(temp_interval)


def process_results(results):
    """Process results depending on its length and return.

    Args:
        results (list): A list of final results.

    Returns:
        The final result of the equation.

    """
    if len(results) == 0:
        return EmptySet
    elif len(results) == 1:
        return results[0]
    else:
        return results[0].union(results[1])


def auto_solve(eq, var_name, low=0, high=1, left_open=True, right_open=True):
    """Automatically solve the equation.

    Args:
        eq (str): The equation to be solved.
        var_name (str): The name of the variable. E.g. "a".
        low (float): The lower bound of the variable.
        high (float): The upper bound of the variable.
        left_open (bool): True if the bound is open on the left.
        right_open (bool): True if the bound is open on the right.

    Returns:
        The solution of the equation.

    """
    if eq == "" or eq.isspace():
        raise ValueError("Please do not enter an empty string.")

    equation = f"+{eq}"
    value_term = get_value_term(equation)
    minmax_terms = get_minmax_terms(equation)
    cons_var_terms = get_cons_var_terms(equation)
    minmax_replace_zeros(minmax_terms)

    if len(minmax_terms) == 0:
        # If there are no minmax_terms, it becomes a linear equation.
        return solve_linear_eq(cons_var_terms, value_term, low, high,
                               left_open, right_open)

    set_points = find_set_points(minmax_terms, var_name)
    if len(set_points) == 0:
        # If there are no set_points, it means there are no
        # variables in minmax_terms, such as min(20, 30) or
        # min(20, 0*a).
        return solve_no_minmax_var(minmax_terms, cons_var_terms, value_term)

    intervals = create_intervals(set_points)
    results = []
    for interval in intervals:
        # Find the intersect because the set points pay no regards to
        # required intervals.
        interval = find_intersect(interval, low, high, left_open, right_open)
        knitted_solver = knit_solver(interval, minmax_terms,
                                     cons_var_terms, "a")
        result = reformat_and_solve(knitted_solver, value_term)
        if result is S.Complexes:
            # If this interval satisfies the equation, check two end
            # points and union them if necessary.
            append_interval_complexes(interval, eq, low, high, results)
        elif result is EmptySet:
            # Skip to the next iteration.
            continue
        elif get_next(result) in interval:
            # If it's a FiniteSet and falls in the interval, return.
            return result
        elif get_next_eval(result) == interval.start \
                or get_next_eval(result) == interval.end:
            # If the result falls on either end point, check the other
            # end point and union it if necessary.
            append_interval_endpoints(interval, eq, result, results, low, high)
        else:
            # For all other cases, skip.
            continue
    return process_results(results)
