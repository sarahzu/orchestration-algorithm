import random

from termcolor import colored

from strategy.strategy_algorithm import StrategyAlgorithm


class JacobiAlgorithm(StrategyAlgorithm):

    def __init__(self):
        super().__init__()

    def algorithm(self, min_state, state, max_state, agent_simulator_object_list, agent_simulator_name_list,
                  initial_input, time_step):
        next_simulator_input = initial_input
        while min_state <= state < max_state:
            for agent_simulator, agent_simulator_name in zip(agent_simulator_object_list, agent_simulator_name_list):
                # execute simulator B with output from simulator A
                simulator_output = self.execute_simulator_with_output_from_other_simulator(
                    agent_simulator, next_simulator_input, agent_simulator_name, state)
                print(str(agent_simulator_name) + " output: " + str(simulator_output))
                next_simulator_input = simulator_output
            # increase state by the given time step
            state += time_step
        return state, next_simulator_input

    # def jacobi(self, a, x, b, current_step):
    #     n = len(x)
    #     x_out = [0] * len(x)
    #     k = 0
    #     k_max = 5
    #     while k < k_max:
    #         for i in range(n):
    #             delta = 0
    #             for j in range(n):
    #                 if not i == j:
    #                     delta = delta + a[i][j] * x[j]
    #                     # x[i] = x[i] - a[i][j] * x_old[j]
    #             try:
    #                 # x[i] = x[i] / a[i][i]
    #                 x_out[i] = (1/a[i][i]) * (b[i] - delta)
    #             except ZeroDivisionError:
    #                 a[i][i] += 1
    #                 # x[i] = x[i] / a[i][i]
    #                 x_out[i] = (1/a[i][i]) * (b[i] - delta)
    #         k += 1
    #     return x_out


