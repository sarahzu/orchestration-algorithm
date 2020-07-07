from osbrain import Agent

from simulatorE.modelE import ModelE
from simulator import Simulator


class SimulatorE(Simulator, Agent):

    def __init__(self):
        super().__init__()
        self.modelE = ModelE()

    def get_data(self):
        return self.data

    def run_state(self, state, data):
        output = self.modelE.run(data, state)
        self.data = output
        return output

