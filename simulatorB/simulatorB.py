from osbrain import Agent

from simulatorB.modelB import ModelB
from simulator import Simulator


class SimulatorB(Simulator, Agent):

    def __init__(self, state, data):
        super().__init__(state)
        self.data = data
        self.modelB = ModelB()

    def get_data(self):
        return self.data

    def run_state(self, state, data):
        output = self.modelB.run(data, state)
        self.data = output
        return output
