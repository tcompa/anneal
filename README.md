## anneal
[![Build Status](https://travis-ci.org/tcompa/anneal.svg?branch=master)](https://travis-ci.org/tcompa/anneal)
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.50116.svg)](http://dx.doi.org/10.5281/zenodo.50116)


Anneal implements a general-purpose simulated-annealing optimization algorithm (originally written for a [sudoku solver](https://github.com/tcompa/sudoku_simulated_annealing)).
The optimization procedure is decoupled from the optimization problem, so that it can be used in a large set of different cases.

You can follow [these steps](#install-anneal) to install anneal, or just [give it a try](#give-it-a-try-without-installing) without installing it.

### Install anneal
To install anneal, follow these instructions:

##### Using pip
If you use `pip` as a package manager, anneal can be installed via
```
pip install https://github.com/tcompa/anneal/archive/v1.0.zip
```
(for version 1.0).

##### Manual install
Clone this repository, then use the setup.py script:
```
git clone git@github.com:tcompa/anneal.git .
cd anneal
python setup.py install --record installed_files.txt
```
(the `--record` option is helpful to later uninstall this package).  
**Warning**: this procedure will install the current development version.

##### Give it a try (without installing)
If you prefer not to install this package, just copy the file
[anneal.py](anneal/anneal.py) in your working directory, and proceed as in the [How to use anneal](#how-to-use-anneal) section.

##### Versions and requirements
Anneal is tested on python 2.7 and 3.4.
On python 2.7, the [future](https://pypi.python.org/pypi/future) package is required.  
Some of the examples additionally require [numpy](http://www.numpy.org/) (version >=1.10) and [matplotlib](http://matplotlib.org/) (version >=1.5).

### How to use anneal
First, you need to define a class which describes your optimization problem.
This class needs to include (at least) the following attributes and methods:
+ Attributes:
  + beta: the inverse temperature (could be the 'real' inverse temperature, or an artificial parameter).
  + energy: the quantity which will be minimised.
+ Methods:
  + set_beta(beta): change the value of beta.
  + MC_move(): perform a Monte Carlo move, and return 1 or 0 if this is accepted/rejected.
  + update_MC_parameters(acc_ratio): update the Monte Carlo parameters, trying to keep the acceptance ratio in a reasonable interval.

Then you can import the annealing function via
```python
   from anneal import simulated_annealing
```
and use it on an instance of your class (see examples below).


##### Examples
A simple example of how to use anneal is the following.
First, we define the `Potential_1d` class, as
```python
class Potential_1d(object):
    '''Naive class, to test the simulated-annealing function.
    '''

    def __init__(self):
        self.x = 10.0
        self.beta = 1e8
        self.energy = self.compute_energy(self.x)
        self.dx = 0.2

    def compute_energy(self, _x):
        return 0.5 * _x ** 2 * math.cos(_x) ** 2

    def set_beta(self, beta):
        self.beta = beta

    def update_MC_parameters(self, acc_ratio):
        if acc_ratio < 0.2 and self.dx > 0.01:
            self.dx *= 0.90909090909090909090
        elif acc_ratio > 0.8 and self.dx < 1.0:
            self.dx *= 1.1

    def MC_move(self):
        xnew = random.uniform(self.x - self.dx, self.x + self.dx)
        E_old = self.energy
        E_new = self.compute_energy(xnew)
        dE = E_new - E_old
        if dE < 0.0 or random.random() < math.exp(- self.beta * dE):
            self.x = xnew
            self.energy = E_new
            return 1
        else:
            return 0
```
Then we call the `simulated_annealing` function via
```python
from anneal import simulated_annealing

P = Potential_1d()
ID = 'Vx_1d'
P, E, t = simulated_annealing(P, ID, beta_min=1e-2, beta_max=1e2,
                              cooling_rate=1e-2, n_steps_per_T=1000,
                              quench_to_T0=True, n_steps_T0=5000)
```

The output `E` is a list of the values of the energy during the optimization.

More examples are available in the [examples](examples) directory.

###Note
The simulated-annealing library itself is not optimized in any way, assuming
that the time-consuming part of the code is somewhere in the class defining the
optimization problem (e.g. in the Monte Carlo moves).
