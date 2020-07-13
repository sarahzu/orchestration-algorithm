import copy
import random

from termcolor import colored

from strategy.strategy_algorithm import StrategyAlgorithm


class JacobiAlgorithm(StrategyAlgorithm):

    def __init__(self):
        super().__init__()

    def algorithm(self, min_state, state, max_state, agent_simulator_object_list, agent_simulator_name_list,
                  initial_input_dict, time_step, dependencies, state_history):

        new_input_dict = copy.deepcopy(initial_input_dict)

        states = {}
        try:
            for simulator_name in agent_simulator_name_list:
                states[simulator_name] = state
                # states = [state] * len(agent_simulator_object_list)
        except TypeError:
            print(colored("------------\nagent_simulator_object_list is of type "
                          + str(type(agent_simulator_object_list)) + "\nbut should be of type list"))
            return None, None

        output_state = state + time_step
        while all(min_state <= state < max_state for state in states.values()):
            # extrapolate the models input data
            for agent_name in agent_simulator_name_list:
                extrapolated_input = self.fourier_extrapolation(new_input_dict[agent_name]['data'], state)
                new_input_dict[agent_name]['data'] = extrapolated_input
            # run the models with the input data
            for agent_simulator, agent_simulator_name in zip(agent_simulator_object_list, agent_simulator_name_list):
                # check on which inputs from other models the current model depends on
                curr_simulator_input = []
                for dependency in dependencies[agent_simulator_name]:
                    # gather the input data
                    new_data = new_input_dict[dependency]['data']
                    curr_simulator_input.append(new_data)

                # define current state and input for current model
                current_simulators_state = states[agent_simulator_name]
                new_input = {"state": current_simulators_state, "data": curr_simulator_input}

                prev_simulator_input = new_input

                # execute simulator B with output from simulator A
                simulator_output = self.execute_simulator_with_output_from_other_simulator(
                    agent_simulator, new_input, agent_simulator_name, time_step)
                print(str(agent_simulator_name) + " output: " + str(
                    simulator_output))  # + " prev output: " + str(prev_simulator_input))

                new_input_dict[agent_simulator_name] = simulator_output

                # increase simulators state
                try:
                    states[agent_simulator_name] += time_step
                except IndexError:
                    print(colored("\n-----warning: state could not be increased------\n", "red"))

                # update state history with new data
                new_history_state = copy.deepcopy(new_input_dict)
                state_history[output_state] = new_history_state

            output_state += time_step

        return states, state_history

