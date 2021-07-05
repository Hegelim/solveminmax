class ConsVarTerm:
    def __init__(self, cons_var_tuple):
        self._operator = cons_var_tuple[0]
        self._coef = cons_var_tuple[1]
        self._var = cons_var_tuple[2]

    def operator(self):
        return self._operator

    def coef(self):
        return self._coef

    def var(self):
        return self._var
