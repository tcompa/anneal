'''
program: anneal_glm.py
author: tc
created: 2016-04-19 -- 10 CEST
notes: performs one simulated-annealing run, for a GLM problem.
'''

import numpy
import matplotlib.pyplot as plt

from lib_simulated_annealing import simulated_annealing
from lib_general_linear_model import GLM

# define D-dimensional General Linear Model: Y=M*X+Q
D = 25
Q = numpy.random.uniform(-1.0, 1.0, D)
M = numpy.random.uniform(-1.0, 1.0, size=(D, D))

# generate noisy data
Npoints = 100
eps = 0.1
X = numpy.random.uniform(-1.0, 1.0, (Npoints, D))
Y = numpy.matmul(X, M) + Q
Y += numpy.random.uniform(-eps, eps, size=Y.shape)

# initialize GLM instance
G = GLM(X, Y)

# perform annealing
print 'SA start'
G, E, et = simulated_annealing(G, 'GLM',
                               beta_min=1e-1, beta_max=1e4,
                               cooling_rate=5e-2, n_steps_per_T=200,
                               quench_to_T0=True, n_steps_T0=10000)
print 'SA end (elapsed: %.1f s)' % et


# plot energy
fig, ax = plt.subplots(1, 1)
ax.plot(E)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('time')
ax.set_ylabel('energy')
plt.savefig('fig_energy.png', bbox_inches='tight')
plt.close()

# plot M
fig, axs = plt.subplots(2, 2, figsize=(10, 10))
ax1, ax2, ax3, ax4 = axs.flatten()
vmin = min(M.min(), G.M0.min(), G.M.min()) / 1.05
vmax = max(M.max(), G.M0.max(), G.M.max()) * 1.05
props = {'cmap': 'viridis', 'vmin': vmin, 'vmax': vmax, 'origin': 'lower'}

im1 = ax1.matshow(M, **props)
im2 = ax2.matshow(G.M, **props)
im3 = ax3.matshow(G.M0, **props)
im4 = ax4.matshow(M - G.M, **props)
ax1.set_title('\"true\"')
ax2.set_title('final')
ax3.set_title('starting')
ax4.set_title('diff')
for ax in axs.flatten():
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_label_position('bottom')
ax_cb = fig.add_axes([0.25, 0.95, 0.5, 0.025])
CB = fig.colorbar(im1, cax=ax_cb, orientation='horizontal')
CB.ax.tick_params(labelsize=10, direction='in',
                  labeltop='on', labelbottom='off')
CB.ax.xaxis.set_ticks_position('top')
CB.ax.xaxis.set_label_position('top')
CB.ax.xaxis.labelpad = 10
plt.savefig('fig_matrix.png', bbox_inches='tight', dpi=128)
plt.close()

# plot Q
plt.plot(G.Q0, 'o-', label='starting')
plt.plot(Q, 'x-', ms=8, label='\"true\"')
plt.plot(G.Q, 'o-', ms=5, label='final')
plt.legend(loc='best')
plt.xlabel('component')
plt.title('offset Q')
plt.savefig('fig_offset.png', bbox_inches='tight')
