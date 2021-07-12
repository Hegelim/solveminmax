## The `solveminmax` Python Package
[![Github All Releases](https://img.shields.io/pypi/v/solveminmax)]()
[![Github All Releases](https://img.shields.io/github/license/Hegelim/solve-sum-minmax)]()
[![Github All Releases](https://img.shields.io/github/v/release/Hegelim/solve-sum-minmax)]()
[![Github All Releases](https://img.shields.io/github/downloads/Hegelim/solve-sum-minmax/total)]()
[![Github All Releases](https://img.shields.io/github/issues/Hegelim/solve-sum-minmax)]()
[![Github All Releases](https://img.shields.io/readthedocs/solveminmax)]()

`solveminmax` is a Python module that allows you to solve a sum of min/max equations
by taking advantage of the powerful `sympy` library.  
For instance, you can solve `min(400, 500x) + min(200, 500x) + min(0, 500x) = 700`
with the assumption that x is within range (0, 1).
****
**Documentation**:
https://solveminmax.readthedocs.io/en/latest/
****
**Legacy Note**:  
From v0.1.0, the former module, `solve-sum-minmax` was renamed to `solveminmax`
so that it follows the Python naming conventions.  
****
**Quick Start**:  
Let's say you want to solve the equation
min(500, 600a) + max(400, 500a) = 500. However, solving it in Math means you
would have to set up the conditions, then solve the check for each one of them,
which sounds like a lot of work, especially for smart people like you
who know how to take advantage of existing tools. So you ask yourself,
"What if there is a library that lets me solve it like a piece of cake?" Well,
there is a library for you now! First off, you need to install it via pip
in your terminal like below:  
```
pip install solveminmax
```
Or, you can directly clone the project in your local repo and install it using
setup.py like below:
```
git clone https://github.com/Hegelim/solveminmax.git
python setup.py install
```
Then to solve your problem, simply type in these
codes in your Python console:
```
>>> from solveminmax import solver
>>> eq = "min(500, 600*a) + max(400, 500*a) = 500"
>>> solver.auto_solve(eq, "a")
FiniteSet(1/6)
```
Whola! In fact, this is a pretty complex problem, but
you just solved it with 3 lines of code. But hold on, what does it mean?
Let's break it down: the core function
`auto_solve` takes in two required parameters
`equation` and `var_name`. `equation` takes in a string of the equation you want to solve
and `var_name` lets you define your variable with flexibility, such as `"a"`
or `"x"`, although currently, it only supports `"a"`.
You can also pass in `"low"`, `"high"`, which lets you specify the range
of your variable. Further details are included in the docstring
if you are interested.  
****
**Perks**:  
* **Fast**: the module solves a set of complex min and max equations usually
  under 100 ms, depending on your hardware.
For example, for an equation as complex as below, it takes 7 ms on average to
  give you a solution:

```
>>> from solveminmax import solver
>>> eq = "max(600*a, 400) + min(200*a, 500) + min(100, 300*a) + 50*a = 600"
>>> %timeit solver.auto_solve(eq, "a")
FiniteSet(4/11)
7.1 ms ± 225 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```
* **Accurate**: it handles exact Rational numbers and intervals.
* **Flexible**：you have a lot of flexibility in defining your equation,
  see below.

* **Versatile**: start from `v0.1.4`, you can plot your equation and check your
results visually. An example is:

```
>>> from solveminmax import plot
>>> eq = "-2*min(300, 400*a) = -600"
>>> plot.make_plot(eq, "a")
```
****
**Version history**:
Version | Core Ideas | Return Rationals | Return Intervals | Error Handling | Plotting
------------ | ------------- | ------------- | ------------- | ------------- | -------------
v0.0.1 | numerical methods | No | No | No | No
v0.0.2 | numerical methods | No | No | No | No
v0.0.3 | combinations | Yes | No | No | No
v0.0.4 | intervals | Yes | Yes | No | No
v0.1.0 | intervals | Yes | Yes | Yes | No
v0.1.4 | intervals | Yes | Yes | Yes | Yes

For more information, check the documentation.
****
**Contact**:  
* **Email**: yz4175@columbia.edu
* **Collaboration**: collaborations are welcomed, please email me if you
are interested.
