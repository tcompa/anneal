#!/usr/bin/python

'''
program: lib_sudoku.py
author: tc
created: 2015-12-06 -- 20 CEST
'''

# imports for python 2/3 compatibility
from __future__ import print_function
from builtins import range
from builtins import object

import numpy
import random
import math


class Sudoku(object):
    '''
    Members:
        scheme     : 9x9 numpy array of integers
        energy
        beta
    Methods:
        __init__(input_file, seed=0)
        _load_puzzle(filename)
        _fill_puzzle()
        _get_box(i, j)
        _total_energy()
        _local_energy(i ,j)
        set_beta()
        MC_move()
        print_puzzle()
    '''

    def __init__(self, input_file, seed=0):
        '''
        Initializes an instance of the Sudoku class.
        Arguments:
            input_file : file with the puzzle
            seed*      : seed for the random-number generator (if 0, a random
                         value is chosen as seed)
        '''
        print('[sudoku] init')
        if seed == 0:
            seed = random.randrange(99999999)
        random.seed(seed)
        print('[sudoku] random seed: %i' % seed)
        # initialize and fill puzzle
        self._load_puzzle(input_file)
        self._fill_puzzle()
        assert self.puzzle.min() >= 1
        assert self.puzzle.max() <= 9
        # initialize other members
        self.energy = self._total_energy()
        self.beta = 1.0e4

    def _load_puzzle(self, filename):
        ''' Reads puzzle from input file.
        '''
        x = numpy.loadtxt(filename, dtype=numpy.int)
        assert x.shape == (9, 9), 'ERROR: wrong-shape puzzle in %s' % filename
        assert x.max() <= 9, 'ERROR: puzzle.max() = %i' % x.max()
        assert x.min() >= 0, 'ERROR: puzzle.min() = %i' % x.min()
        self.puzzle = x[:, :]
        number_clues = (x > 0).sum()
        print('[sudoku] read puzzle from %s (%i clues)' % (filename,
                                                           number_clues))

    def _fill_puzzle(self):
        ''' Replaces zeros with random numbers in [1,..,9].
        '''
        tot = list(range(1, 10)) * 9
        for n in self.puzzle[numpy.nonzero(self.puzzle)].flatten():
            tot.pop(tot.index(n))
        self.non_clues = []
        for i in range(9):
            for j in range(9):
                if not self.puzzle[i, j]:
                    self.non_clues.append([i, j])
                    self.puzzle[i, j] = tot.pop(random.randrange(len(tot)))
        assert tot == [], 'ERROR, in _fill_puzzle()'
        assert self.puzzle.min() > 0, 'ERROR, in _fill_puzzle()'

    def _get_box(self, i, j):
        ''' Returns entries of the 3x3 box for the cell (i, j).
        '''
        return self.puzzle[(i // 3) * 3:(i // 3 + 1) * 3,
                           (j // 3) * 3:(j // 3 + 1) * 3]

    def _total_energy(self):
        ''' Computes the total energy of a puzzle.
        '''
        E = 0
        list_i = list(range(9))
        list_j = [0, 3, 6, 1, 4, 7, 2, 5, 8]
        for ind in range(9):
            E += self._local_energy(list_i[ind], list_j[ind])
        return E

    def _local_energy(self, i, j):
        ''' Computes the local energy of the cell (i, j).
        '''
        E = 0
        # check row
        row = self.puzzle[i, :]
        occupations = numpy.bincount(row)
        occupations = occupations[occupations > 1]
        E += sum(occupations)
        # check column
        column = self.puzzle[:, j]
        occupations = numpy.bincount(column)
        occupations = occupations[occupations > 1]
        E += sum(occupations)
        # check box
        box = self._get_box(i, j).flatten()
        occupations = numpy.bincount(box)
        occupations = occupations[occupations > 1]
        E += sum(occupations)
        return E

    def set_beta(self, beta):
        ''' Sets a new value of beta.
        '''
        self.beta = beta

    def update_MC_parameters(self, dummy):
        pass

    def MC_move(self):
        '''
        Proposes to replace one of the non-fixed cells with a random entry, and
        accepts/rejects according to Metropolis rule.
        '''
        i, j = random.choice(self.non_clues)
        E_ij_old = self._local_energy(i, j)
        n_old = self.puzzle[i, j]
        self.puzzle[i, j] = random.randrange(1, 10)
        E_ij_new = self._local_energy(i, j)
        dE = E_ij_new - E_ij_old
        if dE < 0.0 or random.uniform(0.0, 1.0) < math.exp(- self.beta * dE):
            self.energy += dE
            return 1
        else:
            self.puzzle[i, j] = n_old
            return 0

    def print_puzzle(self):
        for i in range(9):
            for j in range(9):
                print(self.puzzle[i, j], end=' ')
            print()


if __name__ == '__main__':
    S = Sudoku('puzzle.dat', seed=1)
    S.print_puzzle()
