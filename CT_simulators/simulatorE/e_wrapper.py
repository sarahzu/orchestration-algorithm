import copy

from CT_simulators.simulatorE.modelE import ModelE
from hybrid_wrapper import HybridWrapper


class EWrapper(HybridWrapper):
    """
    Wrapper class combining a DE model with this CT model
    """

    def __init__(self):
        self.model = ModelE()

    def run(self, data_list, state):
        """
        run this CT model with transformed DE input

        :param data_list:   (list) input DE data
        :param state:       (int)  current state
        :return:
        """

        initial_data = self.model.get_data()
        try:
            initial_data[0] -= data_list[0][0]
        except Exception:
            initial_data[0] -= data_list[0]
        ct_data = initial_data
        transformed_input = copy.deepcopy(ct_data)
        output = self.model.run(ct_data)
        result = {"output": output, "transformed input": transformed_input}
        return result
