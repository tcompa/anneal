This folder includes three examples of the use of anneal.

Two optimization problems are considered:
 + [lib_potential_1d.py](lib_potential_1d.py) defines a one-dimensional potential, with several local minima.
 + [lib_general_linear_model.py](lib_general_linear_model.py) defines a [Generalized Linear Model](https://en.wikipedia.org/wiki/Generalized_linear_model), for which one wants to perform maximum-likelihood estimation of the parameters.

The full examples are:
+ [anneal_potential1d_single_run.py](anneal_potential1d_single_run.py): performs a single simulated-annealing run, for the optimization of the one-dimensional potential.
+ [anneal_potential1d_many_runs.py](anneal_potential1d_many_runs.py): performs several simulated-annealing runs, for the optimization of the one-dimensional potential. The cooling is set to be fast on purpose, to stress that not all runs will find the global minimum.
+ [anneal_glm.py](anneal_glm.py): performs a single simulated-annealing run, for the GLM problem.
