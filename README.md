**About**:  
`solve-sum-minmax` is used to solve a sum of min/max equations in python by 
taking advantage of the powerful sympy library. For instance, say you want to solve this equation: 
min(400, 500x) + min(200, 500x) + min(0, 500x) = 700 
with the assumption that
x is within range (0, 1).  
In Math, the rigorous way would 
require you to set up all possible conditions, which 
might result in huge computation. 
Currently, there aren't any available packages in Python
that allows you to solve this kind of equation fastly and efficiently. Thus,
this package is developed to fill the void and hopefully be of use to the broad population.  
****
**Quick Start**:  
Let's say you want to solve the equation 
min(500, 600a) + max(400, 500a) = 500. However, solving it in Math means you 
would have to set up the conditions, then solve the check for each one of them, 
which sounds like a lot of work, especially for smart people like you 
who knows how to take advantage of existing tools. So you ask yourself,
"What if there is a library that lets me solve it like a piece of cake?" Well, 
there is a library for you now! First off, you need to install it with 
a few lines like below: 
```
pip install solve-sum-minmax
```
Then to solve your problem, simply type in these
codes below: 
```
from solve-sum-minmax import solver
>>> eq = "min(500, 600*a) + max(400, 500*a) = 500"
>>> solver.auto_solve(eq, "a")
FiniteSet(1/6)
```
Dang, that's so cool😆😆! In fact, this is a pretty complex problem, but 
you just solved it with 3 lines of code. But wait, what does it mean? 
Let's break it down: the core function 
`auto_solve` takes in two required parameters 
`equation` and `var_name`. `equation` takes in a string of the equation you want to solve 
and `var_name` lets you define your variable with flexibility, such as `"a"`
or `"x"`. You can also pass in `"low"`, `"high"`, which 
lets you specify the range of your variable. Further details 
are in the docstring if you are interested.  
****
**Features in 0.0.4**: 
* Now the module is able to return exact values as fractions, such as 1/6.
* Now the module fully supports interval solutions, represented by 
  the powerful Interval object in sympy.
* When there isn't a solution, the function would return `None`. 
* you can put the variable either in the first place inside the parenthesis 
or in the second place. 
* you can use min and max together in one equation.
* you can use + or -. 
* you can have constants in front of min or max, such as 2*min(400, 400a).
****
**Limitations**:  
* Currently, the module only supports `"a"` as the variable. 
* Because the module heavily depends on regular expressions, 
  the user needs to follow the format of the 
equation carefully, or the module might break.
* The equation must be univariate, i.e., there can only be one independent 
variable. 
****
**Contact**:  
* **Email**: yz4175@columbia.edu
* **Collaboration**: collaborations are welcomed, please send me an email if you 
are interested.
