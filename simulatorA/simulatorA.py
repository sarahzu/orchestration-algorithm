from osbrain import Agent

from simulatorA.modelA import ModelA
from simulator import Simulator


class SimulatorA(Simulator, Agent):
    """
    Specific simulator class for the model A
    """

    def __init__(self):
        super().__init__()
        self.modelA = ModelA()

    def get_data(self):
        return self.data

    def run_state(self, state, data):
        """
        start execution of model A

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (list)   model output data list
        """
        output = self.modelA.run(data, state)
        self.data = output
        return output

