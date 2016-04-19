'''
program: anneal_potential1d_many_runs.py
author: tc
created: 2016-04-19 -- 12 CEST
notes: performs several simulated-annealing runs.
'''

import numpy
import matplotlib.pyplot as plt

from lib_potential_1d import Potential_1d
from anneal import simulated_annealing


xmin = []
for run in range(20):
    P = Potential_1d()
    ID = 'Vx_1d_many_runs'
    P, _, _ = simulated_annealing(P, ID, beta_min=1e-2, beta_max=1e2,
                                  cooling_rate=0.2, n_steps_per_T=50,
                                  quench_to_T0=False)
    xmin.append(P.x)

# plot histogram
plt.hist(xmin, bins=20, range=[-10.0, 10.0], normed=True, alpha=0.8)
# plot potential
x = numpy.linspace(-10.0, 10.0, 1000)
Vx = numpy.array([P.compute_energy(j) for j in x])
plt.plot(x, Vx / 100.0, 'r', lw=2, label='$V(x)$')
# finalize plot
plt.grid()
plt.xlim(-10.0, 10.0)
plt.title('Simulated-annealing results for $\\min V(x)$')
plt.xlabel('$x$', fontsize=18)
plt.legend(loc='best')
plt.savefig('fig_example_many_runs.png')
plt.show()
