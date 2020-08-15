import copy

from CT_simulators.simulatorLG.modelLG import ModelLG
from hybrid_wrapper import HybridWrapper


class LGWrapper(HybridWrapper):

    def __init__(self):
        self.model = ModelLG()

    def run(self, ct_data, state):
        transformed_input = copy.deepcopy(ct_data)
        output = self.model.run(ct_data, state)
        result = {"output": output, "transformed input": transformed_input}
        return result
