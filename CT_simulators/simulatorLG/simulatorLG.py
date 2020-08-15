from osbrain import Agent

from CT_simulators.simulatorLG.LG_wrapper import LGWrapper
from simulator import Simulator


class SimulatorLG(Simulator, Agent):
    """
    Specific simulator class for the model D
    """

    def __init__(self):
        super().__init__()
        self.wrapper = LGWrapper()

    def run_state(self, state, data):
        """
        start execution of model D

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (list)   model output data list
        """
        output = self.wrapper.run(data, state)
        return output
