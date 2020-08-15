from osbrain import Agent

from CT_simulators.simulatorB.b_wrapper import BWrapper
from simulator import Simulator


class SimulatorB(Simulator, Agent):
    """
    Specific simulator class for the model B
    """

    def __init__(self):
        super().__init__()
        self.wrapper = BWrapper()

    def run_state(self, state, data):
        """
        start execution of model B

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (list)   model output data list
        """
        output = self.wrapper.run(data, state)
        return output
