*********
Examples
*********

The module supports several kinds of equations that involve minimum and maximum.
To begin with, it supports linear equations without min/max terms:

.. code-block:: python

   >>> from solveminmax import solver
   >>> eq = "10*a = 150"
   >>> solver.auto_solve(eq, "a")
   FiniteSet(15)

It handles general minimum and maximum equations well and returns exact answers
including Rationals and intervals:


.. code-block:: python

  >>> from solveminmax import solver
  >>> eq_1 = "min(400, 600*a) = 400"
  >>> solver.auto_solve(eq_1, "a")
  Interval.Ropen(0.666666666666667, 1)
  >>> eq_2 = "min(500, 600*a) + max(400, 500*a) = 500"
  >>> solver.auto_solve(eq_2, "eq")
  FiniteSet(1/6)

For equations that have no solutions, the module returns :code:`None`:

.. code-block:: python

   >>> from solveminmax import solver
   >>> eq_1 = "min(400*a, 100) = 500"
   >>> print(solver.auto_solve(eq_1, "a"))
   >>> None

It also supports basic error-handling, such as:

.. code-block:: python

   >>> from solveminmax import solver
   >>> eq_1 = "min(20*a) = 300"
   >>> solver.auto_solve(eq_1, "a")
   ValueError: MinMax terms malformed!
