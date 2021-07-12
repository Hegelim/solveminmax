Quick Start
***********
Say someday you encountered a Math problem that looks like this:

:math:`\text{min(500, 600*a) + max(400, 500*a) = 500}`

You know that to solve it by hand, you would have to find all the possible
intervals, the cross-check for each one of them. But now, you can simply
solve it like below in your Python console:

.. code-block:: python

   >>> from solveminmax import solver
   >>> eq = "min(500, 600*a) + max(400, 500*a) = 500"
   >>> solver.auto_solve(eq, "a")
   FiniteSet(1/6)

Whola! In fact, this is a pretty complex problem, but
you just solved it with 3 lines of code. But hold on, what does it mean?
Let's break it down:

The core function
:code:`auto_solve` takes in two required parameters
:code:`equation` and :code:`var_name`. :code:`equation` takes in a string of the equation you want to solve
and :code:`var_name` lets you define your variable with flexibility, such as :code:`"a"`
or :code:`"x"`, although currently, it only supports :code:`"a"`.
You can also pass in :code:`low`, :code:`high`, which lets you specify the range
of your variable. Further details are included in the docstring
if you are interested.
