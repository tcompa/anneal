This folder includes some examples of the use of anneal.

Thre optimization problems are considered:
 + In [one-dimensional pontential](one_dimensional_potential), we want to find the minimum of a function of a single one-dimensional variable.
   + [lib_potential_1d.py](one_dimensional_potential/lib_potential_1d.py): defines the potential (which is chosen to have several local minima).
   + [anneal_potential1d_single_run.py](one_dimensional_potential/anneal_potential1d_single_run.py): performs a single simulated-annealing run.
   + [anneal_potential1d_many_runs.py](one_dimensional_potential/anneal_potential1d_many_runs.py): performs several simulated-annealing runs. The cooling is set to be fast on purpose, to stress that not all runs are guaranteed to find the global minimum.
 + A [sudoku instance](sudoku):
   + class
   + solver
 + The problem of parameters fitting for a Generalized Linear Model (GLM):
   + [lib_generalize_linear_model.py](generalized_linear_model/lib_generalize_linear_model.py) defines a [Generalized Linear Model](https://en.wikipedia.org/wiki/Generalized_linear_model), for which one wants to perform maximum-likelihood estimation of the parameters.
   + [anneal_glm.py](generalized_linear_model/anneal_glm.py): performs a single simulated-annealing run, for the GLM problem.
