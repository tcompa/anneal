'''
program: anneal_potential1d_single_run.py
author: tc
created: 2016-04-19 -- 12 CEST
notes: performs one simulated-annealing run.
'''

from lib_potential_1d import Potential_1d
from anneal import simulated_annealing


P = Potential_1d()
ID = 'Vx_1d'
print 'Simulated annealing start'
P, E, et = simulated_annealing(P, ID, beta_min=1e-2, beta_max=1e2,
                               cooling_rate=1e-2, n_steps_per_T=500,
                               quench_to_T0=True, n_steps_T0=2000)
print 'Simulated annealing end (elapsed time: %.1f s)' % et
print 'Initial energy: %f' % E[0]
print 'Final energy:   %f' % E[-1]
