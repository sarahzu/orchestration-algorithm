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
        Gauss-Seidel coupling algorithm. Work only with two dual dependent models!
        The first model's output is extrapolated and the extrapolated value is then used as input for the next model.
        The next model's output is then interpolated and used as input for the first model's input.

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

        input_dict_with_extrapolation_and_interpolation = copy.deepcopy(initial_input_dict)

        states = {}
        # store current state for every simulator
        for simulator_name in agent_simulator_name_list:
            states[simulator_name] = state

        # increase state in order to compute the next state
        output_state = state + time_step
        # compute each state
        while all(min_state <= state < max_state for state in states.values()):
            order_count = 0
            # go through each simulator
            for agent_simulator, agent_simulator_name in zip(agent_simulator_object_list, agent_simulator_name_list):
                curr_simulator_input = []
                # check on which inputs from other models the current model depends on
                for simulator_name_of_dependency in dependencies[agent_simulator_name]:
                    # if the model runs first, extrapolate
                    if order_count == 0:
                        extrapolated_value = self.extrapolate(
                            input_dict_with_extrapolation_and_interpolation[simulator_name_of_dependency]['output data']
                        )
                        curr_simulator_input.append(extrapolated_value)
                    # if the model runs second, interpolate
                    elif order_count == 1:
                        interpolated_value = self.interpolation(
                            input_dict_with_extrapolation_and_interpolation[simulator_name_of_dependency]['output data']
                        )
                        curr_simulator_input.append(interpolated_value)
                    else:
                        # gather the input data normally
                        input_data = \
                            state_history[states[agent_simulator_name]][simulator_name_of_dependency]['output data']
                        curr_simulator_input.append(input_data)

                # define current state and input for current model
                current_simulators_state = states[agent_simulator_name]
                new_input = {"state": current_simulators_state, "output data": curr_simulator_input}

                # execute current simulator with output from its dependent on simulator
                simulator_output = self.execute_simulator_with_output_from_other_simulator(
                    agent_simulator, new_input, agent_simulator_name, time_step)

                input_dict_with_extrapolation_and_interpolation[agent_simulator_name] = simulator_output

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
                new_history_state = copy.deepcopy(input_dict_with_extrapolation_and_interpolation)
                state_history[output_state] = new_history_state

                order_count += 1

            output_state += time_step

        return states, state_history
