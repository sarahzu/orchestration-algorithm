from osbrain import Agent

from DE_simulators.simulatorCiw.CT_to_DE_wrapper import CtToDeWrapper
from simulator import Simulator


class SimulatorCiw(Simulator, Agent):
    """
    Specific simulator class for the CIW model
    """

    def __init__(self):
        super().__init__()
        self.wrapper = CtToDeWrapper()

    def run_state(self, state, data):
        """
        run function for a model using the CIW library

        :param state: (int)  current state of the simulation
        :param data:  (list) previously computed data
        :return       (dict) model output data dictionary in the form
                             {'output': [0.011261392881117818], 'transformed input': 1}
        """
        output = self.wrapper.run(data, state)
        return output
