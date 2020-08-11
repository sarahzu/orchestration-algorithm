from CT_Simulators.simulatorLG.modelLG import ModelLG
from hybrid_wrapper import HybridWrapper


class LGWrapper(HybridWrapper):

    def __init__(self):
        self.model = ModelLG()

    def run(self, ct_data, state):
        output = self.model.run(ct_data, state)
        result = {"output": output, "transformed input": ct_data}
        return result
