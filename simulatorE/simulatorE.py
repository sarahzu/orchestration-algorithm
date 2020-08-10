from osbrain import Agent

from simulatorE.modelE import ModelE
from simulator import Simulator


class SimulatorE(Simulator, Agent):
    """
    Specific simulator class for the model E
    """

    def __init__(self):
        super().__init__()
        self.modelE = ModelE()

    def run_state(self, state, data):
        """
        start execution of model E

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (list)   model output data list
        """
        output = self.modelE.run(data, state)
        return output

