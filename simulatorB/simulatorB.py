from osbrain import Agent

from simulatorB.modelB import ModelB
from simulator import Simulator


class SimulatorB(Simulator, Agent):
    """
    Specific simulator class for the model B
    """

    def __init__(self):
        super().__init__()
        self.modelB = ModelB()

    def run_state(self, state, data):
        """
        start execution of model B

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (list)   model output data list
        """
        output = self.modelB.run(data, state)
        return output
