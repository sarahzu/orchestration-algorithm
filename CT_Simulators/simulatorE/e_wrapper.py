from CT_Simulators.simulatorE.modelE import ModelE
from hybrid_wrapper import HybridWrapper


class EWrapper(HybridWrapper):

    def __init__(self):
        self.model = ModelE()

    def run(self, data_list, state):
        initial_data = self.model.get_data()
        initial_data[0] -= data_list[0][0]
        ct_data = initial_data
        output = self.model.run(ct_data)
        return output