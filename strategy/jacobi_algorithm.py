from termcolor import colored

from strategy.strategy_algorithm import StrategyAlgorithm


class JacobiAlgorithm(StrategyAlgorithm):

    def __init__(self):
        super().__init__()

    def algorithm(self, min_state, state, max_state, agent_simulator_object_list, agent_simulator_name_list,
                  initial_input, time_step):
        try:
            outputs = [initial_input] * len(agent_simulator_object_list)
        except TypeError:
            print(colored("------------\nagent_simulator_object_list is of type "
                          + str(type(agent_simulator_object_list)) + "\nbut should be of type list"))
            return None, None

        i = 0
        while min_state <= state < max_state:
            for agent_simulator, agent_simulator_name in zip(agent_simulator_object_list, agent_simulator_name_list):
                current_simulators_input = outputs[i]
                # execute simulator B with output from simulator A
                simulator_output = self.execute_simulator_with_output_from_other_simulator(
                    agent_simulator, current_simulators_input, agent_simulator_name, state)
                print(str(agent_simulator_name) + " output: " + str(simulator_output))
                outputs[i] = simulator_output
                i += 1
            # increase state by the given time step
            state += time_step
            i = 0
        return state, outputs[i]
