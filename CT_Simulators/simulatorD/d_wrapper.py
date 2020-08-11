from CT_Simulators.simulatorD.modelD import ModelD
from hybrid_wrapper import HybridWrapper


class DWrapper(HybridWrapper):

    def __init__(self):
        self.model = ModelD()

    def run(self, data_list, state):
        initial_data = self.model.get_data()
        initial_data[0] += data_list[0][1] + data_list[1][0]
        initial_data[1] -= data_list[0][1] + data_list[1][0]
        ct_data = initial_data
        output = self.model.run(ct_data, state)
        return output
