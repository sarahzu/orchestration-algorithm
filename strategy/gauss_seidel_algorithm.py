import copy

from termcolor import colored

from strategy.strategy_algorithm import StrategyAlgorithm


class GaussSeidelAlgorithm(StrategyAlgorithm):

    def __init__(self):
        super().__init__()

    def algorithm(self, min_state, state, max_state, agent_simulator_object_list,
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

        output_state = state + time_step
        while all(min_state <= state < max_state for state in states.values()):
            count = 0
            prev_agent_name = ""
            for agent_simulator, agent_simulator_name in zip(agent_simulator_object_list, agent_simulator_name_list):
                curr_simulator_input = []
                # check on which inputs from other models the current model depends on
                for simulator_name_of_dependency in dependencies[agent_simulator_name]:
                    # first exrapolate
                    if count == 0:
                        extrapolated_value = self.extrapolate(
                            new_input_dict[simulator_name_of_dependency]['output data'])
                        curr_simulator_input.append(extrapolated_value)
                    # second intrapolate
                    elif count == 1:
                        interpolated_value = self.interpolation(
                            new_input_dict[simulator_name_of_dependency]['output data'],
                            new_input_dict[simulator_name_of_dependency]['output data'])
                        curr_simulator_input.append(interpolated_value)
                    else:
                        # gather the input data
                        new_data = state_history[states[agent_simulator_name]][simulator_name_of_dependency]['output data']
                        curr_simulator_input.append(new_data)

                # define current state and input for current model
                current_simulators_state = states[agent_simulator_name]
                new_input = {"state": current_simulators_state, "output data": curr_simulator_input}

                # execute simulator with output from other simulator(s)
                simulator_output = self.execute_simulator_with_output_from_other_simulator(
                    agent_simulator, new_input, agent_simulator_name, time_step)
                #  print(str(agent_simulator_name) + " output: " + str(simulator_output))

                new_input_dict[agent_simulator_name] = simulator_output

                # increase simulators state
                try:
                    states[agent_simulator_name] += time_step
                except IndexError:
                    print(colored("\n-----warning: state could not be increased------\n", "red"))

                # if count == 0:
                #     new_input_dict[agent_simulator_name]['extrapolated input'] = extrapolated_value
                # elif count == 1:
                #     new_input_dict[agent_simulator_name]['interpolated input'] = interpolated_value

                # update state history with new data
                new_history_state = copy.deepcopy(new_input_dict)

                state_history[output_state] = new_history_state

                count += 1

            output_state += time_step

        return states, state_history
