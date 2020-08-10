from osbrain import Agent

from simulatorC.modelC import ModelC
from simulator import Simulator


class SimulatorC(Simulator, Agent):
    """
    Specific simulator class for the model C
    """

    def __init__(self):
        super().__init__()
        self.modelC = ModelC()

    def run_state(self, state, data):
        """
        start execution of model C

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (list)   model output data list
        """
        output = self.modelC.run(data, state)
        return output

