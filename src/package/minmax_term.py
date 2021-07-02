import re


class MinMaxTerm:
    def __init__(self, minmax_term):
        """minmax_term is a tuple that looks like ('+', '', 'min', '(400, 400*a)')"""
        self._operator = minmax_term[0]
        self._coef = minmax_term[1]
        self._minmax_op = minmax_term[2]
        self._minmax_tuple = minmax_term[3]

    def operator(self):
        return self._operator

    def coef(self):
        return "1" if self._coef == "" else self._coef

    def minmax_op(self):
        return self._minmax_op

    def minmax_tuple(self):
        return self._minmax_tuple

    def left_right_nums(self):
        match = re.findall(r"\s*(\d+).*,\s*(\d+)\s*", self._minmax_tuple)
        return float(match[0][0]), float(match[0][1])

    def left_right_half(self):
        match = re.findall(r"\s*(\d+.*),\s*(\d+[^\)]*)\s*", self._minmax_tuple)
        return match[0][0], match[0][1]
