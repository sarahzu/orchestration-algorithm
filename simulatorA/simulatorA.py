from osbrain import Agent

from simulatorA.modelA import ModelA
from simulator import Simulator


class SimulatorA(Simulator, Agent):

    def __init__(self, state, time_step, data):
        super().__init__(state, time_step)
        self.data = data
        self.modelA = ModelA()

        # TODO: While loop
        # if time_step:
        #    self.run_time_step(self.time_step, data)

    def get_data(self):
        return self.data

    def run_time_step(self, time_step, data):
        output = self.modelA.run(data, time_step)
        self.data = output
        return output

