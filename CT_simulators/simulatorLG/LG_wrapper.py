import copy

from CT_simulators.simulatorLG.modelLG import ModelLG
from hybrid_wrapper import HybridWrapper


class LGWrapper(HybridWrapper):
    """
    Wrapper class combining another CT model with this CT model
    """

    def __init__(self):
        self.model = ModelLG()

    def run(self, ct_data, state):
        """
        run this CT model with other models CT input

        :param ct_data:   (list) input CT data
        :param state:     (int)  current state
        :return:
        """
        transformed_input = copy.deepcopy(ct_data)
        output = self.model.run(ct_data, state)
        result = {"output": output, "transformed input": transformed_input}
        return result
