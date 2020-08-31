import copy

from hybrid_wrapper import HybridWrapper
from CT_simulators.simulatorHMM.modelHMM import ModelHMM


class DeToCtWrapper(HybridWrapper):
    """
    Wrapper class combining a DE model with this CT model
    """

    def __init__(self):
        self.model = ModelHMM()

    def run(self, de_data, state):
        """
        run this CT model with transformed DE input

        :param de_data:   (list) input DE data
        :param state:     (int)  current state
        :return:
        """
        ct_data = self.model.get_data()
        ct_data[0] += de_data[0][0]
        ct_data[1] -= de_data[0][0]
        ct_data[2] += de_data[0][0]
        ct_data[3] -= de_data[0][0]
        transformed_input = copy.deepcopy(ct_data)
        output = self.model.run(ct_data)
        result = {"output": output, "transformed input": transformed_input}
        return result

