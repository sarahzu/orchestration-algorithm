import copy

from DE_simulators.simulatorA.modelA import ModelA
from hybrid_wrapper import HybridWrapper


class AWrapper(HybridWrapper):
    """
    Wrapper class combining a CT model with this DE model
    """

    def __init__(self):
        self.model = ModelA()

    def run(self, ct_data, state):
        """
        run this DE model with transformed CT input

        :param ct_data:   (list) input CT data
        :param state:     (int)  current state
        :return:
        """
        try:
            de_data = ct_data[0][0] + ct_data[1]
        except TypeError:
            de_data = ct_data[0][0] + ct_data[1][0]
        output = [self.model.run(de_data, state)]
        transformed_input = copy.deepcopy(de_data)
        result = {"output": output, "transformed input": transformed_input}
        return result
