************
Format Guide
************

Because the module depends heavily on regular expressions, please follow
the guide on how to define your equations carefully, or the module might break.
In a nutshell, open up your Python console and wrap the equation you want to
solve in a string with the format similar to the example:

.. code-block:: python

    >>> eq = "max(600*a, 400) + min(200*a, 500) + min(100, 300*a) + 50*a = 600"

Before we delve into explanations in details, let's define a few terms:

*  **value_term**: the value you want to solve your equation for, here it's :code:`600`.
*  **minmax_term**: it is what it means in English, for example, :code:`max(600*a, 400)`.
*  **cons_var_term**: terms with constants times variables, such as :code:`50*a`.

.. note::

   The module does not support constants on the left-hand side of the equation
   just yet, which will be added in future versions. 

In brief, what you **can** do include:

*  put the variable either in the 1st or 2nd place inside the parenthesis.
   For example, either :code:`min(200, 300*a)` or :code:`min(300*a, 200)` is fine.

*  use min and max together in one equation.
* use + and/or -.
* have constants in front of min or max, such as :code:`2*min(400, 400a)`.
* have any space between each component.
* have leading 0s before variable, such as :code:`min(0*a, 200)`.
* have constants inside min or max, such as :code:`min(20, 30)`.

What you **can't** do include:

*  use :code:`==` instead of :code:`=`.
*  for the :code:`cons_var_term`, have variables before constants, such as :code:`a*50`
   instead of :code:`50*a`.
*  missing any necessary parenthesis.
*  use other operators instead of + or -.
*  missing any necessary :code:`*` operator for each variable.
*  put any constants on the left-hand side of the equation. For example, it would
   break if you define your equation as:

   .. code-block:: python

      >>> eq = "20 + max(600*a, 400) + min(100, 300*a) + 50*a = 600"

   Do me a favor, if
   you have any constants, subtract it from the right-hand side and
   rearrange your terms before using the module.
