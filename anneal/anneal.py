'''
program: anneal.py
author: tc
created: 2016-04-19 -- 11 CEST
'''

from __future__ import print_function
from builtins import range
import time

__all__ = ['simulated_annealing']


def simulated_annealing(P, ID, beta_min=1e-2, beta_max=1e2,
                        cooling_rate=1e-2, n_steps_per_T=100,
                        E_min=-float('inf'),
                        quench_to_T0=False, n_steps_T0=1000):
    '''
    General-purpose simulated-annealing optimization function.

    Parameters
    ----------
    P : object
        Instance of a custom class, wich includes attributes
            P.beta
            P.energy
        and methods:
            P.set_beta(beta)
            P.MC_move(), returning 1/0 (accepted/rejected)
            P.update_MC_parameters(acc_ratio)
    ID : str
        Label for the problem under study.
    beta_min : float, optional
        Minimum inverse temperature (default: 1e-2)
    beta_max: float, optional
        Maximum inverse temperature (default: 1e2)
    cooling_rate : float, optional
        Cooling rate (default: 1e-2)
    n_steps_per_T : int, optional
        Number of MC moves attempted at each temperature (default: 100)
    E_min : float, optional
        Global energy minimum, if known (default: -infinity)
    quench_to_T0 : bool, optional
        If True, perform a T=0 quench at the end of the annealing
    n_steps_T0 : int, optional
        Number of MC moves after the T=0 quench

    Returns
    -------
    P : object
        Current version of P
    E : list
        List of the final energies for each temperature
    elapsed_time : float
        Total elapsed time, in seconds

    '''
    # initialize
    time_start = time.clock()
    P.set_beta(beta_min)
    E = []
    out = open('log_sim_ann_%s.dat' % ID, 'w')
    out.write('# start - %s\n' % time.strftime('%c'))
    out.write('# beta_min: %f\n' % beta_min)
    out.write('# beta_max: %f\n' % beta_max)
    out.write('# cooling rate: %f\n' % cooling_rate)
    out.write('# n_steps_per_T %f\n' % n_steps_per_T)
    out.write('# initial energy: %f\n' % P.energy)
    out.write('# quench_to_T0: %s\n' % quench_to_T0)
    out.write('# n_steps_T0: %i\n' % n_steps_T0)
    out.write('#\n')
    out.flush()
    # annealing loop
    while P.beta < beta_max:
        acc = 0
        for step in range(n_steps_per_T):
            acc += P.MC_move()
        acc_ratio = acc / float(n_steps_per_T)
        out.write('%10.4g  %10.4g %.8f\n' % (P.beta, P.energy, acc_ratio))
        out.flush()
        E.append(P.energy)
        if P.energy <= E_min:
            out.write('# reached E_min=%s. Break.\n' % E_min)
            out.flush()
            break
        # update beta and MC parameters
        P.set_beta(P.beta * (1.0 + cooling_rate))
        P.update_MC_parameters(acc_ratio)
    # T=0 quench
    if quench_to_T0:
        out.write('# start T=0 quench\n')
        out.flush()
        P.set_beta(1e24)
        for step in range(n_steps_T0):
            P.MC_move()
        E.append(P.energy)
        out.write('# %12.4g  %10.4g %.8f\n' % (P.beta, P.energy, acc_ratio))
        out.write('# after quench, reached E=%g\n' % P.energy)
        out.flush()
    # finalize
    out.write('# end\n')
    elapsed_time = time.clock() - time_start
    out.write('# elapsed: %.2f s\n' % elapsed_time)
    out.close()
    return P, E, elapsed_time
