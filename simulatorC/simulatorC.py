from osbrain import Agent

from simulatorC.modelC import ModelC
from simulator import Simulator


class SimulatorC(Simulator, Agent):

    def __init__(self, state, data):
        super().__init__(state)
        self.data = data
        self.modelC = ModelC()

    def get_data(self):
        return self.data

    def run_state(self, state, data):
        output = self.modelC.run(data, state)
        self.data = output
        return output

