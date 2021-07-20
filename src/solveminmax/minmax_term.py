import re


class MinMaxTerm:
    """The MinMaxTerm class.

    Attributes:
        _operator (str): The operator of the minmax terms.
        _coef (str): The coefficients for minmax terms.
        _minmax_op (str): Min or max operator of minmax terms.
        _minmax_tuple (str): A string of tuple, such as (30, 30*a).

    """
    def __init__(self, minmax_term):
        """Initialize an MinMaxTerm instance.

        Examples:
            >>> minmax_term = ('+', '', 'min', '(400, 400*a)')
            >>> a = MinMaxTerm(minmax_term)

        Args:
            minmax_term (tuple): A tuple of minmax term.

        """
        self._operator = minmax_term[0]
        self._coef = minmax_term[1]
        self._minmax_op = minmax_term[2]
        self._minmax_tuple = minmax_term[3]

    def operator(self):
        """Get the operator.

        Examples:
            >>> minmax_term = ('+', '', 'min', '(400, 400*a)')
            >>> a = MinMaxTerm(minmax_term)
            >>> a.operator()
            '+'

        Returns:
            str: The minmax operator.

        """
        return self._operator

    def coef(self):
        """Get the coefficient of minmax terms.

        Examples:
            >>> minmax_term = ('+', '2', 'min', '(400, 400*a)')
            >>> a = MinMaxTerm(minmax_term)
            >>> a.operator()
            '2'

        Returns:
            str: The coefficient of the minmax term.

        """
        return "1" if self._coef == "" else self._coef

    def minmax_op(self):
        """Get the minmax operator (whether min or max)

        Returns:
            str: The minmax operator.

        """
        return self._minmax_op

    def minmax_tuple(self):
        """Get the minmax tuple.

        Returns:
            str: The minmax tuple.

        """
        return self._minmax_tuple

    def left_right_nums(self):
        """Get the left and right numbers in minmax tuple.

        Examples:
            >>> minmax_term = ('+', '2', 'min', '(400, 400*a)')
            >>> a = MinMaxTerm(minmax_term)
            >>> a.left_right_nums()
            (400.0, 400.0)

        Returns:
            tuple: tuple containing left and right float numbers.

        """
        match = re.findall(r"\s*([\+\-]*\d+).*,\s*([\+\-]*\d+)\s*",
                           self._minmax_tuple)
        return float(match[0][0]), float(match[0][1])

    def left_right_half(self):
        """Get the left and right half from minmax tuple.

        Examples:
            >>> minmax_term = ('+', '2', 'min', '(400, 400*a)')
            >>> a = MinMaxTerm(minmax_term)
            >>> a.left_right_half()
            ('400', '400*a')

        Returns:
            tuple: The left and right string in minmax tuple.

        """
        match = re.findall(r"\s*([\-]*\d+.*),\s*([\-]*\d+[^\)]*)\s*",
                           self._minmax_tuple)
        if len(match) != 0:
            return match[0][0], match[0][1]
        else:
            raise ValueError("MinMax terms malformed!")
