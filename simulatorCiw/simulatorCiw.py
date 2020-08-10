from osbrain import Agent

from simulator import Simulator
from simulatorCiw.CT_to_DE_wrapper import CtToDeWrapper


class SimulatorCiw(Simulator, Agent):

    def __init__(self):
        super().__init__()
        self.wrapper = CtToDeWrapper()

    def run_state(self, state, data):
        """
        run function for a model using the CIW library

        :param state: (int)  current state of the simulation
        :param data:  (list) previously computed data
        """
        output = self.wrapper.run(data, state)
        return output
