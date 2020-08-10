from statistics import median

import matplotlib.pyplot as plt
import numpy as np
from hmmlearn import hmm


class ModelHMM:

    def __init__(self):
        self.data = [0.6, 0.3, 0.1, 0.0]

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def run(self, data_list):
        """
        CT model cenerating sample points from a Hiden Markov Model (HMM)

        code taken and modified from:
        https://hmmlearn.readthedocs.io/en/latest/auto_examples/plot_hmm_sampling.html#sphx-glr-auto-examples-plot-hmm-sampling-py
        last visited: 09.08.2020

        :param data_list:   (list) input data list
        :return:            (list) output data list
        """
        # multiplier = 0
        # if len(data_list) == 1:
        #     if len(data_list[0]) == 1:
        #         multiplier = data_list[0][0]
        #     else:
        #         multiplier = data_list[0][state]
        # else:
        #     for data_points in data_list:
        #        multiplier += data_points[state]

        # startprob = np.array([0.6, 0.3, 0.1, 0.0])
        startprob = np.array(data_list)
        # The transition matrix, note that there are no transitions possible
        # between component 1 and 3
        transmat = np.array([[0.7, 0.2, 0.0, 0.1],
                             [0.3, 0.5, 0.2, 0.0],
                             [0.0, 0.3, 0.5, 0.2],
                             [0.2, 0.0, 0.2, 0.6]])
        # The means of each component
        means = np.array([[0.0, 0.0],
                          [0.0, 11.0],
                          [9.0, 10.0],
                          [11.0, -1.0]])
        # The covariance of each component
        covars = .5 * np.tile(np.identity(2), (4, 1, 1)) # * multiplier

        # Build an HMM instance and set parameters
        model = hmm.GaussianHMM(n_components=4, covariance_type="full")

        # Instead of fitting it from the data, we directly set the estimated
        # parameters, the means and covariance of the components
        model.startprob_ = startprob
        model.transmat_ = transmat
        model.means_ = means
        model.covars_ = covars

        # Generate samples
        X, Z = model.sample(5)
        result = []
        for np_array in X:
            result.append([np_array[0], np_array[1]])
            # result.append(median(np_array))
        # self.data = result
        return result

