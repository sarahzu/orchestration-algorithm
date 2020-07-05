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
