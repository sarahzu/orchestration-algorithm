import numpy as np
from hybrid_wrapper import HybridWrapper
from DE_simulators.simulatorCiw.modelCiw import ModelCiw


class CtToDeWrapper(HybridWrapper):

    def __init__(self):
        self.model = ModelCiw()

    def run(self, ct_data, state):
        data = np.array(ct_data)
        data_median = np.median(data)

        if data_median > 0:
            event = 1
        else:
            event = -1

        output = self.model.run(event, state)
        return [output]