from simulatorB.modelB import ModelB
from simulator import Simulator


class SimulatorB(Simulator):

    def __init__(self, state, time_step):
        super().__init__(state, time_step)
        self.modelB = ModelB()

        # TODO: While loop
        if time_step:
            self.run_time_step(self.time_step, "")

    def run_time_step(self, time_step, data):
        output = self.modelB.run()

        return output
