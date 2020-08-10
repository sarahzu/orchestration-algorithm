from osbrain import Agent

from simulatorD.modelD import ModelD
from simulator import Simulator


class SimulatorD(Simulator, Agent):
    """
    Specific simulator class for the model D
    """

    def __init__(self):
        super().__init__()
        self.modelD = ModelD()

    def run_state(self, state, data):
        """
        start execution of model D

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (list)   model output data list
        """
        output = self.modelD.run(data, state)
        return output

