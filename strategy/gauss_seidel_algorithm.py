from termcolor import colored

from strategy.strategy_algorithm import StrategyAlgorithm


class GaussSeidelAlgorithm(StrategyAlgorithm):

    def __init__(self):
        super().__init__()

    def algorithm(self, min_state, state, max_state, agent_simulator_object_list, agent_simulator_name_list,
                  initial_input, time_step):

        next_simulator_input = initial_input
        try:
            states = [state] * len(agent_simulator_object_list)
        except TypeError:
            print(colored("------------\nagent_simulator_object_list is of type "
                          + str(type(agent_simulator_object_list)) + "\nbut should be of type list"))
            return None, None

        while min_state <= state < max_state:
            i = 0
            for agent_simulator, agent_simulator_name in zip(agent_simulator_object_list, agent_simulator_name_list):
                current_simulators_state = states[i]
                # execute simulator B with output from simulator A
                simulator_output = self.execute_simulator_with_output_from_other_simulator(
                    agent_simulator, next_simulator_input, agent_simulator_name, current_simulators_state)
                print(str(agent_simulator_name) + " output: " + str(simulator_output))
                next_simulator_input = simulator_output

                # increase simulators state and states index
                states[i] += time_step
                i += 1

            # increase state by the given time step
            state += time_step

        return state, next_simulator_input

    # simulator_order = {1: simulatorA, 2: simulatorB, ...}
    # agent_simulator_object_list = [agent_simulatorB, agent_simulatorA]
    # def algo_2(self, max_state, time_step, agent_simulator_object_list, agent_simulator_name_list,
    #            simulator_order, curr_simulator_input):
    #     state = 0
    #     uc = [0] * len(agent_simulator_object_list)
    #     y = [0] * len(agent_simulator_object_list)
    #     up = [0] * len(agent_simulator_object_list)
    #
    #     #  initial variables
    #     for w_i, w in enumerate(agent_simulator_object_list):
    #         uc[w_i] = 0
    #         y[w_i] = 0
    #         up[w_i] = 0
    #     # compute initial outputs
    #     for j in range(len(agent_simulator_object_list)):
    #         # simulator input
    #         uc[j] = curr_simulator_input
    #         y[j] = uc[j]
    #         curr_simulator_input = y[j]
    #         up[j] = uc[j]
    #
    #     while state < max_state:
    #         for j in range(len(agent_simulator_object_list)):
    #             w = simulator_order[j]
    #             # simulator input
    #             uc[j] = curr_simulator_input
    #             print("uc: " + str(uc[j]))
    #
    #             # do step
    #             y[j] = self.execute_simulator_with_output_from_other_simulator(
    #                 w, uc[j], agent_simulator_name_list[j], state)
    #
    #             curr_simulator_input = y[j]
    #         for w in range(agent_simulator_object_list):
    #             up[w] = uc[w]
    #         state += time_step
    #     return y


