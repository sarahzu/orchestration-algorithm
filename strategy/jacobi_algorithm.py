import copy
import random

from termcolor import colored

from strategy.strategy_algorithm import StrategyAlgorithm


class JacobiAlgorithm(StrategyAlgorithm):

    def __init__(self):
        super().__init__()

    def algorithm(self, min_state, state, max_state, agent_simulator_object_list, agent_simulator_name_list,
                  initial_input_dict, time_step, dependencies, state_history):
        """
        Jacobi implementation of coupling algorithm. First, all simulators inputs at the next state are going to be
        extrapolated. This extrapolated value is then used to run the current simulation state.

        :param min_state:                       (int)  smallest state possible
        :param state:                           (int)  current simulation state
        :param max_state:                       (int)  biggest state possible
        :param agent_simulator_object_list:     (list) list containing all simulator objects used in this simulation
        :param agent_simulator_name_list:       (list) list containing all simulator names used in this simulation
        :param initial_input_dict:              (dict) initial input data used at the start of the coupling algorithm
                                                       in the form: {simulator: {state:0, data:[...]}, ...}
        :param time_step:                       (int)  passed time between two states
        :param dependencies:                    (dict) dictionary containing all dependency information in the form
                                                       {simulator:[dependent_on_simulator1, dependent_on_simulator2, ...], ...}
        :param state_history:                   (dict) history dictionary containing all computed data in every
                                                       simulation state in the form:
                                                       {0:{simulator: {state:0, data:[...]}, ...}, 1: {...}}
        :return: states, state_history          (list) list of all computed states
                                                (dict) and history dictionary containing all computed data
        """

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
                new_input_dict[agent_name]['data'] = self.extrapolate(new_input_dict[agent_name]['data'])

            #  run the models with the input data
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

                # execute current simulator with output from its dependent on simulators
                simulator_output = self.execute_simulator_with_output_from_other_simulator(
                    agent_simulator, new_input, agent_simulator_name, time_step)
                # print(str(agent_simulator_name) + " output: " + str(simulator_output))

                # add newly computed output to stored inputs
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
