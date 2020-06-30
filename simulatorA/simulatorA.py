from osbrain import Agent

from simulatorA.modelA import ModelA
from simulator import Simulator


class SimulatorA(Simulator, Agent):

    def __init__(self, state, data):
        super().__init__(state)
        self.data = data
        self.modelA = ModelA()

    def get_data(self):
        return self.data

    def run_time_step(self, state, data):
        output = self.modelA.run(data, state)
        self.data = output
        return output

