from osbrain import Agent

from simulatorD.modelD import ModelD
from simulator import Simulator


class SimulatorD(Simulator, Agent):

    def __init__(self):
        super().__init__()
        self.modelD = ModelD()

    def get_data(self):
        return self.data

    def run_state(self, state, data):
        output = self.modelD.run(data, state)
        self.data = output
        return output

