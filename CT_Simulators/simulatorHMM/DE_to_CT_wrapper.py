from hybrid_wrapper import HybridWrapper
from CT_Simulators.simulatorHMM.modelHMM import ModelHMM


class DeToCtWrapper(HybridWrapper):

    def __init__(self):
        self.model = ModelHMM()

    def run(self, de_data, state):
        ct_data = self.model.get_data()
        ct_data[0] += de_data[0][0]
        ct_data[1] -= de_data[0][0]
        ct_data[2] += de_data[0][0]
        ct_data[3] -= de_data[0][0]
        output = self.model.run(ct_data)
        return output

