'''
created: 2016-01-27
author: tc
'''

from builtins import object
from anneal import simulated_annealing


class test_simulated_annealing(object):

    def test_sim_ann(self):

        class empty_problem_class(object):

            def __init__(self):
                self.energy = 0.0
                self.beta = 0.0

            def set_beta(self, beta):
                self.beta = beta

            def MC_move(self):
                return 1

            def update_MC_parameters(self, acc_ratio):
                pass

        P = empty_problem_class()
        ID = 'ID'
        P, E, time = simulated_annealing(P, ID, beta_min=1.0, beta_max=2.0,
                                         cooling_rate=0.1, n_steps_per_T=10)

    def test_sim_ann_with_T0_quench(self):

        class empty_problem_class(object):

            def __init__(self):
                self.energy = 0.0
                self.beta = 0.0

            def set_beta(self, beta):
                self.beta = beta

            def MC_move(self):
                return 1

            def update_MC_parameters(self, acc_ratio):
                pass

        P = empty_problem_class()
        ID = 'ID'
        P, E, time = simulated_annealing(P, ID, beta_min=1.0, beta_max=2.0,
                                         cooling_rate=0.1, n_steps_per_T=10,
                                         quench_to_T0=True, n_steps_T0=10)
