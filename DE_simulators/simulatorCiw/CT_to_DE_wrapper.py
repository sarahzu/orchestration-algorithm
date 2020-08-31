import copy

import numpy as np
from hybrid_wrapper import HybridWrapper
from DE_simulators.simulatorCiw.modelCiw import ModelCiw


class CtToDeWrapper(HybridWrapper):
    """
    Wrapper class combining a CT model with this DE model
    """

    def __init__(self):
        self.model = ModelCiw()

    def run(self, ct_data, state):
        """
        run this DE model with transformed CT input

        :param ct_data:   (list) input CT data
        :param state:     (int)  current state
        :return:
        """
        data = np.array(ct_data)
        data_median = np.median(data)

        if data_median > 0:
            event = 1
        else:
            event = -1
        transformed_input = copy.deepcopy(event)

        output = [self.model.run(event, state)]
        result = {"output": output, "transformed input": transformed_input}
        return result
