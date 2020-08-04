import copy

from termcolor import colored

from strategy.strategy_algorithm import StrategyAlgorithm


class GaussSeidelAlgorithm(StrategyAlgorithm):

    def __init__(self):
        super().__init__()

    def algorithm(self, min_state, state, max_state, agent_simulator_object_list, agent_simulator_name_list,
                  initial_input_dict, time_step, dependencies, state_history):
        """
        Gauss-Seidel implementation of coupling algorithm. The sequence of the executed simulators is predefined and
        extrapolation is used to guess future state outputs and interpolation is used to make the outcome more accurate.

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

        prev_simulator_input = initial_input_dict
        states = {}
        try:
            for simulator_name in agent_simulator_name_list:
                states[simulator_name] = state
                # states = [state] * len(agent_simulator_object_list)
        except TypeError:
            print(colored("------------\nagent_simulator_object_list is of type "
                          + str(type(agent_simulator_object_list)) + "\nbut should be of type list"))
            return None, None

        print("ob list: " + str(agent_simulator_name_list))

        output_state = state + time_step
        while all(min_state <= state < max_state for state in states.values()):
            count = 0
            for agent_simulator, agent_simulator_name in zip(agent_simulator_object_list, agent_simulator_name_list):
                # check on which inputs from other models the current model depends on
                curr_simulator_input = []
                for simulator_name_of_dependency in dependencies[agent_simulator_name]:
                    # gather the input data

                    # first exrapolate or extrapolate if no interpolation has taken place
                    if states[simulator_name_of_dependency] != state:
                        dependency_data = state_history[state][simulator_name_of_dependency]['data']
                        extrapolated_new_input = self.extrapolate(dependency_data)
                        dependency_data.append(extrapolated_new_input)
                        curr_simulator_input.append(dependency_data)
                        print("extra: " + str(curr_simulator_input))

                    # then interpolate
                    else:
                        dependency_data = state_history[state][simulator_name_of_dependency]['data']
                        next_state_dependency_data = \
                        state_history[states[agent_simulator_name]][simulator_name_of_dependency]['data']
                        interpolated_new_input = self.interpolation(dependency_data, next_state_dependency_data)
                        next_state_dependency_data[-1] = interpolated_new_input
                        curr_simulator_input.append(next_state_dependency_data)
                        print("inter: " + str(curr_simulator_input))

                # define current state and input for current model
                current_simulators_state = states[agent_simulator_name]
                new_input = {"state": current_simulators_state, "data": curr_simulator_input}

                # execute current simulator with output from depended on simulator
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

                count += 1

            output_state += time_step

        return states, state_history

    def algorithm_dual_dependency(self, min_state, state, max_state, agent_simulator_object_list,
                                  agent_simulator_name_list, initial_input_dict, time_step, dependencies,
                                  state_history):
        """
        Gauss-Seidel coupling algorithm but with only dual dependent models.

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

        prev_simulator_input = initial_input_dict
        states = {}
        try:
            for simulator_name in agent_simulator_name_list:
                states[simulator_name] = state
                # states = [state] * len(agent_simulator_object_list)
        except TypeError:
            print(colored("------------\nagent_simulator_object_list is of type "
                          + str(type(agent_simulator_object_list)) + "\nbut should be of type list"))
            return None, None

        print("ob list: " + str(agent_simulator_name_list))

        output_state = state + time_step
        while all(min_state <= state < max_state for state in states.values()):
            count = 0
            prev_agent_name = ""
            for agent_simulator, agent_simulator_name in zip(agent_simulator_object_list, agent_simulator_name_list):
                # first exrapolate
                if count == 0:
                    extrapolated_new_input = self.extrapolate(new_input_dict[agent_simulator_name]['data'])
                    new_input_dict[agent_simulator_name]['data'].append(extrapolated_new_input)
                # second intrapolate
                elif count == 1:
                    intrapolated_new_input = self.interpolation(new_input_dict[prev_agent_name]['data'],
                                                                new_input_dict[agent_simulator_name]['data'])
                    new_input_dict[agent_simulator_name]['data'].append(intrapolated_new_input)

                # check on which inputs from other models the current model depends on
                curr_simulator_input = []
                for dependency in dependencies[agent_simulator_name]:
                    # gather the input data
                    new_data = state_history[states[agent_simulator_name]][dependency]['data']
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

                count += 1
                prev_agent_name = agent_simulator_name

            output_state += time_step

        return states, state_history
