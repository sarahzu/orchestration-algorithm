from osbrain import Agent

from CT_simulators.simulatorLG.LG_wrapper import LGWrapper
from simulator import Simulator


class SimulatorLG(Simulator, Agent):
    """
    Specific simulator class for the logistic growth model
    """

    def __init__(self):
        super().__init__()
        self.wrapper = LGWrapper()

    def run_state(self, state, data):
        """
        start execution of logistic growth model

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (dict)   model output data dictionary in the form
                                 {'output': [0.09948076960399241, 0.0],
                                 'transformed input': [[[-0.17307679866920092, -1.0046970164746332], ...]]}
        """
        output = self.wrapper.run(data, state)
        return output
