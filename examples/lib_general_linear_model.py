#!/usr/bin/python

'''
program: lib_general_linear_model.py
author: tc
created: 2016-04-19 -- 9:30 CEST
'''

import random
import numpy
import math

from builtins import object   # python 2/3 compatibility


class GLM(object):
    '''
    asdasd
    '''

    def __init__(self, x_points, y_points, Q0=None, M0=None):

        # problem parameters
        self.x = x_points.copy()
        self.y = y_points.copy()
        self.N, self.D = self.x.shape
        assert self.x.shape == self.y.shape

        # MC parameters and initialization
        self.dQ = 0.005
        self.dM = 0.005
        if Q0 is not None:
            self.Q = Q0
        else:
            self.Q = numpy.zeros(self.D)
        if M0 is not None:
            self.M = M0
        else:
            self.M = numpy.eye(self.D)
        self.Q0 = self.Q.copy()
        self.M0 = self.M.copy()

        # initialization
        self.energy = self.compute_energy(self.Q, self.M)
        self.beta = 1e8

    def compute_energy(self, Q, M):
        dev_squ_i = ((self.y - (numpy.matmul(self.x, M) + Q)) ** 2).sum(axis=1)
        return dev_sq_i.mean()

    def set_beta(self, beta):
        self.beta = beta

    def update_MC_parameters(self, acc_ratio):
        if acc_ratio < 0.2 and self.dM > 0.001:
            self.dM *= 0.90909090909090909090
        elif acc_ratio > 0.8 and self.dM < 2.0:
            self.dM *= 1.1
        if acc_ratio < 0.2 and self.dQ > 0.001:
            self.dQ *= 0.90909090909090909090
        elif acc_ratio > 0.8 and self.dQ < 2.0:
            self.dQ *= 1.1

    def MC_move(self):
        Mnew = self.M.copy()
        Qnew = self.Q.copy()
        if random.uniform(0.0, 1.0) < 0.7:
            row = random.randrange(self.D)
            Mnew[row, :] += numpy.random.uniform(-self.dM, self.dM,
                                                 size=self.D)
        else:
            Qnew += numpy.random.uniform(-self.dQ, self.dQ, Qnew.shape)
        E_old = self.energy
        E_new = self.compute_energy(Qnew, Mnew)
        dE = E_new - E_old
        if dE < 0.0 or random.random() < math.exp(- self.beta * dE):
            self.M = Mnew.copy()
            self.Q = Qnew.copy()
            self.energy = E_new
            return 1
        else:
            return 0
