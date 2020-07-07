from osbrain import Agent

from simulatorC.modelC import ModelC
from simulator import Simulator


class SimulatorC(Simulator, Agent):

    def __init__(self):
        super().__init__()
        self.modelC = ModelC()

    def get_data(self):
        return self.data

    def run_state(self, state, data):
        output = self.modelC.run(data, state)
        self.data = output
        return output

