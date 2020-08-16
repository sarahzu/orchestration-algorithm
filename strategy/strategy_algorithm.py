import copy
import json
import statistics
from statistics import median


class StrategyAlgorithm:

    def __init__(self):
        pass

    def algorithm(self, min_state, state, max_state, agent_simulator_object_list, agent_simulator_name_list,
                  initial_input, time_step, dependencies, state_history):
        """
        abstract function defining each algorithm strategy's algorithm function.

        :param min_state:                       (int)  smallest state possible
        :param state:                           (int)  current simulation state
        :param max_state:                       (int)  biggest state possible
        :param agent_simulator_object_list:     (list) list containing all simulator objects used in this simulation
        :param agent_simulator_name_list:       (list) list containing all simulator names used in this simulation
        :param initial_input:                   (dict) initial input data used at the start of the coupling algorithm
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
        pass

    def execute_simulator_with_output_from_other_simulator(self, agent_simulator_receiver, simulator_sender_input,
                                                           agent_sender_name, time_step):
        """
        Execute a receiver agent with input from a sender simulator's agent

        :param agent_simulator_receiver:    (agent)  simulator to be executed and which receives input
        :param simulator_sender_input:      (dict)   input for receiving agent coming from the sending agent
                                                     in the form: {state: 0, data: [...]}
        :param agent_sender_name:           (string) name of sending agent
        :param time_step                    (int)    passed time between two states
        :return:                            (dict)   output data computed with executed simulator
                                                     in the form: {state: 0, data: [...]}
        """
        agent_simulator_receiver.send(agent_sender_name, json.dumps(simulator_sender_input))
        simulator_receiver_output_data = agent_simulator_receiver.recv(agent_sender_name)
        try:
            simulator_receiver_output = {
                # "state": simulator_sender_input['state'] + time_step,
                "input data": simulator_sender_input['output data'],
                "transformed input data": simulator_receiver_output_data['transformed input'],
                "output data": simulator_receiver_output_data['output']
            }
        except TypeError:
            simulator_receiver_output = {
                # "state": simulator_sender_input['state'] + time_step,
                "input data": simulator_sender_input['output data'],
                "transformed input data": [],
                "output data": simulator_receiver_output_data
            }
        return simulator_receiver_output

    def extrapolate(self, input_data):
        """
        Extrapolation function. It computes the next data entry by taking the median of all data entry spaces.

        :param input_data:  (list or int) data to extrapoalte
        :return:            (lsit or int) next computed value
        """
        # output_data_list = []
        # for k,v in input_data.items():
        #     for simulator, value in v.items():
        #         output_data_list.append(value['output data'])
        # print("list: " + str(output_data_list))

        # differences = []
        try:
            for i, data in enumerate(input_data):
                # differences.append(input_data[i+1] - data)
                input_data[i] += 1
            # input_data.append(input_data[-1] + median(differences))
            return input_data
        except (IndexError, TypeError) as e:
            try:
                for i, data in enumerate(input_data):
                    input_data[i][0] += 1
                return input_data
            except (IndexError, TypeError) as e:
                return input_data + 1

    # def extrapolate2(self, model_values_1, model_values_2, state):
    #     # given values
    #     xi = np.array(model_values_1)
    #     yi = np.array(model_values_2)
    #     f = interpolate.interp1d(xi, yi, fill_value='extrapolate')
    #     return f(state)

    def interpolation(self, input_data_prev, input_data_post):
        """
        Interpolation function. It computes the value inbetween the last elements of the two given data lists.

        :param input_data_prev:     (list) first data list
        :param input_data_post:     (list) second data list
        :return:                    (int) computed value
        """
        # prev_value = input_data_prev[-1]
        # post_value = input_data_post[-1]

        try:
            result = []
            for i, data in enumerate(input_data_prev):
                sub_result = input_data_post[i] + input_data_prev[i]
                result.append(sub_result)
            return result
        except (statistics.StatisticsError, TypeError) as e:
            result = [input_data_post + 2]
            return result

    # # method taken and modified from https://gist.github.com/tartakynov/83f3cd8f44208a1856ce
    # # last visited: 2020-07-13
    # def fourier_extrapolation(self, x, n_predict):
    #     n = len(x)
    #     n_harm = 10  # number of harmonics in model
    #     t = np.arange(0, n)
    #     p = np.polyfit(t, x, 1)  # find linear trend in x
    #     x_notrend = x - p[0] * t  # detrended x
    #     x_freqdom = fft.fft(x_notrend)  # detrended x in frequency domain
    #     f = fft.fftfreq(n)  # frequencies
    #     indexes = range(n)
    #     # sort indexes by frequency, lower -> higher
    #     sorted(indexes, key=lambda i: np.absolute(f[i]))
    #
    #     t = np.arange(0, n + n_predict)
    #     restored_sig = np.zeros(t.size)
    #     for i in indexes[:1 + n_harm * 2]:
    #         ampli = np.absolute(x_freqdom[i]) / n  # amplitude
    #         phase = np.angle(x_freqdom[i])  # phase
    #         restored_sig += ampli * np.cos(2 * np.pi * f[i] * t + phase)
    #
    #     results = restored_sig + p[0] * t
    #     # for i, result in enumerate(results):
    #         # results[i] = round(result)
    #     return results.tolist()
