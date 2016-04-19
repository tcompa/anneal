'''
program: lib_potential_1d.py
author: tc
created: 2016-04-19 -- 12 CEST
notes: Class for one-dimensional potential, to be used in simulated annealing.
'''

import random
import math
from builtins import object   # python 2/3 compatibility


class Potential_1d(object):
    '''
    One-dimensional potential instance.

    Attributes
    ----------
    x : float
        Current configuration.
    energy : float
        Energy of the current configuration.
    beta : float
        Current inverse temperature.
    dx : float
        Step-size for Monte Carlo moves.

    Methods
    -------

    compute_energy()
        Compute energy.
    set_beta(beta)
        Set beta to a new value.
    update_MC_parameters(acc_ratio)
        Update dx.
    MC_move()
        Perform a Monte Carlo move.
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
