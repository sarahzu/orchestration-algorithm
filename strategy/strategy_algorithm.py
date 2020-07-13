import json

import numpy as np
from numpy import fft


class StrategyAlgorithm:

    def __init__(self):
        pass

    def algorithm(self, min_state, state, max_state, agent_simulator_object_list, agent_simulator_name_list,
                  initial_input, time_step, dependencies, state_history):
        pass

    def execute_simulator_with_output_from_other_simulator(self, agent_simulator_receiver, simulator_sender_input,
                                                           agent_sender_name, time_step):
        """
        Execute a receiver agent with input from a sender simulator's agent

        :param agent_simulator_receiver:    simulator to be executed and which receives input
        :param simulator_sender_input:      input for receiving agent coming from the sending agent
        :param agent_sender_name:           name of sending agent
        :param state:                       current time state
        :param time_step                    current time step
        :return:                            json containing the output data computed with executed simulator
        """
        agent_simulator_receiver.send(agent_sender_name, json.dumps(simulator_sender_input))
        simulator_receiver_output_data = agent_simulator_receiver.recv(agent_sender_name)

        simulator_receiver_output = {
            "state": simulator_sender_input['state'] + time_step,
            "data": simulator_receiver_output_data
        }
        return simulator_receiver_output

    # Function to calculate the linear extrapolation
    #   taken and modified from: https://www.geeksforgeeks.org/program-to-implement-linear-extrapolation/
    #   last visited: 2020-07-13)
    def extrapolate(self, history, state, agent_name):
        """

        :param history:     {state0: {agent1: {"state": x, "data": [[...], [...], ...]}}, state1: {...}, ...}
        :param state:
        :return:
        """
        try:
            print(str(history))
            y = (history[state][agent_name]["data"][state][state + 1] + (state - history[state][agent_name]["data"][state][state + 1]) /
                 (history[state][agent_name]["data"][state + 1][state] - history[state][agent_name]["data"][state][state]) *
                 (history[state][agent_name]["data"][state + 1][state + 1] - history[state][agent_name]["data"][state][state + 1]))
        except ValueError:
            return None

        return y

    # method taken and modified from https://gist.github.com/tartakynov/83f3cd8f44208a1856ce
    # last visited: 2020-07-13
    def fourier_extrapolation(self, x, n_predict):
        n = len(x)
        n_harm = 10  # number of harmonics in model
        t = np.arange(0, n)
        p = np.polyfit(t, x, 1)  # find linear trend in x
        x_notrend = x - p[0] * t  # detrended x
        x_freqdom = fft.fft(x_notrend)  # detrended x in frequency domain
        f = fft.fftfreq(n)  # frequencies
        indexes = range(n)
        # sort indexes by frequency, lower -> higher
        sorted(indexes, key=lambda i: np.absolute(f[i]))

        t = np.arange(0, n + n_predict)
        restored_sig = np.zeros(t.size)
        for i in indexes[:1 + n_harm * 2]:
            ampli = np.absolute(x_freqdom[i]) / n  # amplitude
            phase = np.angle(x_freqdom[i])  # phase
            restored_sig += ampli * np.cos(2 * np.pi * f[i] * t + phase)

        results = restored_sig + p[0] * t
        # for i, result in enumerate(results):
            # results[i] = round(result)
        return results.tolist()
