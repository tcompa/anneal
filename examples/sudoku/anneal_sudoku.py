import matplotlib.pyplot as plt

from anneal import simulated_annealing
from lib_sudoku import Sudoku

S = Sudoku('puzzle.dat')
cooling_rate = 1e-2
beta_min = 0.1
beta_max = 5e2
S, E, e_time = simulated_annealing(S, 'Sudoku',
                                   beta_min=beta_min, beta_max=beta_max,
                                   cooling_rate=cooling_rate,
                                   n_steps_per_T=1000, E_min=0)
S.print_puzzle()

plt.xlabel('step', fontsize=18)
plt.ylabel('energy', fontsize=18)
plt.plot(E)
plt.ylim(bottom=0)
plt.savefig('fig_energy.png', bbox_inches='tight')
plt.show()
