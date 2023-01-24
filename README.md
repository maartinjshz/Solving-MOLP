# Solving MOLP
 Algorithms for solving Multi Objective Linear programming (MOLP) problems 


### About

This project provides multiple methods for solving MOLP problems using fuzzy approach. 
The MOLP problems this code can solve are in form: 
$$Max \ \ \ Cx$$
$$s.t. \ Ax \leq b$$
$$x \geq 0$$

The problems are solves using: 

* Agregating Fuzzy Orderings
* Agregating Membership functions 

### Setup

The code uses packages: 

* NumPy
* SciPy
* Pypoman 

And then clone the project. You only need src\SolveMolp folder. Simply call the Optimize.py function with all the necessary input data:

* Method 
* NumPy array for objective function coefficients.
* NumPy array for matrix A values.
* NumPy array for vector b values.
* NummPy array for weights. (If not specified, every function will be asigned weight: 1/N, where N is the number of objective functions.)

Some Examples can be found in Test folder. 

## Refrences: 

[1] O. Grigorenko, Involving fuzzy orders for multi-objective linear programming, Mathematical Modelling and Analysis 17(3) (2012) 366–382.
https://doi.org/10.3846/13926292.2012.685958 

[2] H.-J. Zimmermann. Fuzzy programming and linear programming with several objective functions. Fuzzy Sets and Systems, 1(1):45–55, 1978.
http://dx.doi.org/10.1016/0165-0114(78)90031-3


![Tests](https://github.com/maartinjshz/Solving-MOLP/actions/workflows/tests.yml/badge.svg)
