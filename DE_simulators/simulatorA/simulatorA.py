from osbrain import Agent

from DE_simulators.simulatorA.a_wrapper import AWrapper
from simulator import Simulator


class SimulatorA(Simulator, Agent):
    """
    Specific simulator class for the model A
    """

    def __init__(self):
        super().__init__()
        self.wrapper = AWrapper()

    def run_state(self, state, data):
        """
        start execution of model A

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (dict)   model output data dictionary in the form {'output': [16], 'transformed input': 16}
        """
        output = self.wrapper.run(data, state)
        return output

