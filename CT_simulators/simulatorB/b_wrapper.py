import copy

from CT_simulators.simulatorB.modelB import ModelB
from hybrid_wrapper import HybridWrapper


class BWrapper(HybridWrapper):
    """
    Wrapper class combining a DE model with this CT model
    """

    def __init__(self):
        self.model = ModelB()

    def run(self, de_data, state):
        """
        run this CT model with transformed DE input

        :param de_data: (list) input DE data
        :param state:   (int)  current state
        :return:
        """
        initial_data = self.model.get_data()
        try:
            initial_data[0] += de_data[0]
            initial_data[1] += de_data[1]
        except TypeError:
            initial_data[0] += de_data[0][0]
            initial_data[1] += de_data[1][0]
        ct_data = initial_data
        transformed_input = copy.deepcopy(ct_data)
        output = self.model.run(ct_data, state)
        result = {"output": output, "transformed input": transformed_input}
        return result
