import ciw
from osbrain import Agent

from simulator import Simulator
from simulatorCiw.modelCiw import ModelCiw


class SimulatorCiw(Simulator, Agent):

    def __init__(self):
        super().__init__()
        self.model = ModelCiw()

    def run_state(self, state, data):
        """
        run function for a CIW model

        :param state: (int)  current state of the simulation
        :param data:  (list) previously computed data
        """
        output = self.model.run(data, state)
        self.data = output
        return output
