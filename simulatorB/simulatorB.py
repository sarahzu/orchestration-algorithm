from osbrain import Agent

from simulatorB.modelB import ModelB
from simulator import Simulator


class SimulatorB(Simulator, Agent):

    def __init__(self, state, time_step, data):
        super().__init__(state, time_step)
        self.data = data
        self.modelB = ModelB()

        # TODO: While loop
        #if time_step:
            # self.run_time_step(self.time_step, data)

    def get_data(self):
        return self.data

    def run_time_step(self, time_step, data):
        output = self.modelB.run(data, time_step)
        self.data = output
        return output
