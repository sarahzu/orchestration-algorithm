from CT_Simulators.simulatorB.modelB import ModelB
from hybrid_wrapper import HybridWrapper


class BWrapper(HybridWrapper):

    def __init__(self):
        self.model = ModelB()

    def run(self, de_data, state):
        initial_data = self.model.get_data()
        initial_data[0] += de_data[0][0]
        initial_data[1] += de_data[1][0]
        ct_data = initial_data
        output = self.model.run(ct_data, state)
        return output
