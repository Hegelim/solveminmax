About
*****

| :code:`solveminmax` is a Python module that allows you to solve a sum of min/max equations
 by taking advantage of the powerful :code:`sympy` library. For instance, say you want to
 solve this equation: :math:`\text{min(400, 500x) + min(200, 500x) + min(0, 500x) = 700}`
 with the assumption that x is within range :math:`\text{(0, 1)}`.
| In Math, the rigorous way would
 require you to set up all possible conditions, which
 might result in huge computation.
 Currently, there aren't any available packages in Python
 that allows you to solve this kind of equation fastly and efficiently. Thus,
 this package is developed to fill the void and hopefully be of use to the broad
 population.
