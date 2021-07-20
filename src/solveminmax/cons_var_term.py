class ConsVarTerm:
    """The ConsVarTerm class.

    Attributes:
        _operator (str): The operator of the cons_var_term.
        _coef (str): The coefficient of the cons_var_term.
        _var (str): The variable of the cons_var_term.

    """
    def __init__(self, cons_var_tuple):
        """Initialize a ConsVarTerm object.

        Args:
            cons_var_tuple (tuple): A tuple of cons_var_term.

        Examples:
            >>> cons_var_tuple = ('+', '2', 'a')
            >>> a = ConsVarTerm(cons_var_tuple)

        """
        self._operator = cons_var_tuple[0]
        self._coef = cons_var_tuple[1]
        self._var = cons_var_tuple[2]

    def operator(self):
        """Get the operator of the cons_var_term.

        Returns:
            str: The operator of the cons_var_term.

        """
        return self._operator

    def coef(self):
        """Get the coefficient of the cons_var_term.

        Returns:
            str: The coefficient of the cons_var_term.

        """
        return self._coef

    def var(self):
        """Get the variable of the cons_var_term.

        Returns:
            str: The variable of the cons_var_term.

        """
        return self._var
