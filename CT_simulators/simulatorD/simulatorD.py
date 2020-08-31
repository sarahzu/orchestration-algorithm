from osbrain import Agent

from CT_simulators.simulatorD.d_wrapper import DWrapper
from simulator import Simulator


class SimulatorD(Simulator, Agent):
    """
    Specific simulator class for the model D
    """

    def __init__(self):
        super().__init__()
        self.wrapper = DWrapper()

    def run_state(self, state, data):
        """
        start execution of model D

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (dict)   model output data dictionary in the form
                                 {'output': [50, -11, 82], 'transformed input': [35, 4, 83]}
        """
        output = self.wrapper.run(data, state)
        return output

