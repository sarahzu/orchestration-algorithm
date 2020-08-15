import copy

from DE_simulators.simulatorC.modelC import ModelC
from hybrid_wrapper import HybridWrapper


class CWrapper(HybridWrapper):

    def __init__(self):
        self.model = ModelC()

    def run(self, ct_data, state):
        de_data = ct_data[0][0]
        transformed_input = copy.deepcopy(de_data)
        output = [self.model.run(de_data, state)]
        result = {"output": output, "transformed input": transformed_input}
        return result
