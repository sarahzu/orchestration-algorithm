from osbrain import Agent

from simulator import Simulator
from simulatorCT.modelCT import ModelCT


class SimulatorCT(Simulator, Agent):
    """
    Specific simulator class for the model D
    """

    def __init__(self):
        super().__init__()
        self.model = ModelCT()

    def run_state(self, state, data):
        """
        start execution of model D

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (list)   model output data list
        """
        output = self.model.run(data, state)
        return output
