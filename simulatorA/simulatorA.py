from simulatorA.modelA import ModelA
from simulator import Simulator


class SimulatorA(Simulator):

    def __init__(self, state, time_step):
        super().__init__(state, time_step)
        self.modelA = ModelA()

        # TODO: While loop
        if time_step:
            self.run_time_step(self.time_step, "")

    def run_time_step(self, time_step, data):
        output = self.modelA.run()

        return output

