from osbrain import Agent

from DE_simulators.simulatorC.c_wrapper import CWrapper
from simulator import Simulator


class SimulatorC(Simulator, Agent):
    """
    Specific simulator class for the model C
    """

    def __init__(self):
        super().__init__()
        self.wrapper = CWrapper()

    def run_state(self, state, data):
        """
        start execution of model C

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (dict)   model output data dict in the form {'output': [10], 'transformed input': 10}
        """
        output = self.wrapper.run(data, state)
        return output

