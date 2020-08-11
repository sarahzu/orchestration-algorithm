from DE_simulators.simulatorC.modelC import ModelC
from hybrid_wrapper import HybridWrapper


class CWrapper(HybridWrapper):

    def __init__(self):
        self.model = ModelC()

    def run(self, ct_data, state):
        de_data = ct_data[0][0]
        output = [self.model.run(de_data, state)]
        result = {"output": output, "transformed input": de_data}
        return result
