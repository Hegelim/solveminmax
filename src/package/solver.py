import re
from sympy import S, Symbol, EmptySet, Interval, FiniteSet
from sympy.solvers import solveset
import numpy as np
# TODO: what if the equation starts with a -?
# TODO: what if the interval is infinity on one end?
# TODO: what if there are two numbers inside the min?


def get_minmax_terms(equation):
    """Return a list of tuples. """
    return re.findall(r"(\+|\-)\s*(\d*)\s*\**\s*(min|max)(\([^\)]+\))",
                      equation)


def find_set_points(minmax_terms, var_name, low=0, high=1, left_open=True,
                    right_open=True):
    """Return a list of sorted set points.
    Return an empty list there are variables but all coefficients are 0,
    or there are simply no variables. """
    pts = set()
    for term in minmax_terms:
        match = re.findall(r"\s*(\d+).*,\s*(\d+)\s*", term[3])
        left = float(match[0][0])
        right = float(match[0][1])
        splitted = term[3].split(",")
        if var_name in splitted[0]:
            try:
                pts.add(right / left)
            except ZeroDivisionError:
                continue
        elif var_name in splitted[1]:
            try:
                pts.add(left / right)
            except ZeroDivisionError:
                continue
    return sorted(pts)


def create_intervals(set_points, low=0, high=1, left_open=True,
                     right_open=True):
    """Create a list of intervals based on set_points.
    a < x <= b. """
    intervals = []
    i = -1
    j = 0
    while i < len(set_points):
        if i == -1:
            interval = Interval(low, set_points[j], left_open=left_open,
                                right_open=True)
            if interval is not EmptySet:
                intervals.append(interval)
        elif j == len(set_points):
            interval = Interval(set_points[i], high, left_open=True,
                                right_open=right_open)
            if interval is not EmptySet:
                intervals.append(interval)
        else:
            intervals.append(Interval(set_points[i], set_points[j],
                                      left_open=True, right_open=True))
        i += 1
        j += 1
    return intervals


def get_validate_eq(equation):
    return equation.replace("=", "==")


def get_parts(eq):
    return re.findall(r"[\+\-][^\+\-=]*", eq)


def random_interval(interval):
    return np.random.uniform(interval.start, interval.end)


def get_left_right(minmax_tuple):
    match = re.findall(r"\s*(\d+.*),\s*(\d+[^\)]*)\s*", minmax_tuple)
    return match[0][0], match[0][1]


def get_cons_var_terms(equation):
    match_list = re.findall(r"(\+|\-)\s*(\d+)\s*\*\s*([a-z]+)", equation)
    i = 0
    n = len(match_list)
    while i < len(match_list):
        if "min" in match_list[i][2] or "max" in match_list[i][2]:
            match_list.pop(i)
            i -= 1
            n -= 1
        i += 1
    return match_list


def get_value_term(equation):
    return re.search(r"=\s*(\d+)", equation).group(1)


def knit_solver(interval, minmax_terms, cons_var_terms, var_name):
    solver = ""
    for term in minmax_terms:
        operator = term[0]
        coef = 1 if term[1] == "" else float(term[1])
        minmax = term[2]
        minmax_tuple = term[3]
        if var_name not in minmax_tuple:
            val = eval(f"{minmax}{minmax_tuple}")
            solver += f"{operator}{coef}*{val}"
        else:
            rand = random_interval(interval)
            index = term[3].rfind(var_name)
            replaced = term[3][:index] + "rand" + term[3][index + 1:]
            replaced = f"{minmax}{replaced}"
            left, right = get_left_right(term[3])
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
                solver += f"{operator}{coef}*{var_part}"
            else:
                solver += f"{operator}{coef}*{non_var_part}"
    for term in cons_var_terms:
        solver += f"{term[0]}{term[1]}*{term[2]}"
    return solver


def solve_linear_eq(cons_var_terms, value_term, low, high,
                    left_open, right_open):
    knit = ""
    for cons_var_term in cons_var_terms:
        operator = cons_var_term[0]
        coef = cons_var_term[1]
        variable = cons_var_term[2]
        knit += f"{operator}{coef}*{variable}"
    knit = f"{knit} - {value_term}"
    a = Symbol("a")
    result = solveset(eval(knit), a)
    if result is S.Complexes:
        return result.intersect(Interval(low, high, left_open=left_open,
                                         right_open=right_open))
    else:
        return result


def minmax_replace_zeros(minmax_terms):
    i = 0
    n = len(minmax_terms)
    while i < n:
        operator = minmax_terms[i][0]
        coef = minmax_terms[i][1]
        minmax_op = minmax_terms[i][2]
        paren_term = minmax_terms[i][3]
        left, right = get_left_right(paren_term)
        if "a" in left and "*" in left:
            index = left.find("*")
            num = float(left[:index])
            non_var_term = right
        elif "a" in right and "*" in right:
            index = right.find("*")
            num = float(right[:index])
            non_var_term = left
        else:
            """If the term does not contain variable. """
            i += 1
            continue
        if num == 0:
            minmax_terms[i] = (operator, coef, minmax_op,
                               f"(0,{non_var_term})")
        i += 1


def solve_no_minmax_var(minmax_terms, cons_var_terms, value_term):
    knit = ""
    for term in minmax_terms:
        operator = term[0]
        coef = "1" if term[1] == "" else term[1]
        minmax_op = term[2]
        minmax_tuple = term[3]
        knit += f"{operator}{coef}*{minmax_op}{minmax_tuple}"
    for cons_var_term in cons_var_terms:
        operator = cons_var_term[0]
        coef = cons_var_term[1]
        variable = cons_var_term[2]
        knit += f"{operator}{coef}*{variable}"
    knit = f"{knit} - {value_term}"
    a = Symbol("a")
    return solveset(eval(knit), a)


def auto_solve(eq, var_name, low=0, high=1, left_open=True, right_open=True):
    equation = f"+{eq}"
    value_term = get_value_term(equation)
    minmax_terms = get_minmax_terms(equation)
    cons_var_terms = get_cons_var_terms(equation)
    minmax_replace_zeros(minmax_terms)

    if len(minmax_terms) == 0:
        """If there are no minmax_terms, it becomes a 
        linear equation. """
        return solve_linear_eq(cons_var_terms, value_term,
                               low, high,
                               left_open=left_open,
                               right_open=right_open)

    set_points = find_set_points(minmax_terms, var_name)
    if len(set_points) == 0:
        """If there are no set_points, it means there are no 
        variables in minmax_terms. """
        return solve_no_minmax_var(minmax_terms, cons_var_terms, value_term)

    intervals = create_intervals(set_points)
    results = []
    for interval in intervals:
        interval = interval.intersect(Interval(low, high,
                                               left_open=left_open,
                                               right_open=right_open))
        knitted_solver = knit_solver(interval, minmax_terms,
                                     cons_var_terms, "a")
        knitted_solver = f"{knitted_solver} - {value_term}"
        a = Symbol("a")
        result = solveset(eval(knitted_solver), a)
        if result is S.Complexes:
            temp_interval = interval
            validate_eq = get_validate_eq(eq)
            a = interval.start
            if a != low and eval(validate_eq):
                temp_interval = temp_interval.union(FiniteSet(a))
            a = interval.end
            if a != high and eval(validate_eq):
                temp_interval = temp_interval.union(FiniteSet(a))
            results.append(temp_interval)
        elif result is EmptySet:
            continue
        elif list(result)[0] in interval:
            return result
        elif list(result)[0].evalf() == interval.start:
            a = np.random.uniform(interval.start, interval.end)
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
        elif list(result)[0].evalf() == interval.end:
            a = np.random.uniform(interval.start, interval.end)
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
    if len(results) == 0:
        return None
    elif len(results) == 1:
        return results[0]
    else:
        return results[0].union(results[1])
