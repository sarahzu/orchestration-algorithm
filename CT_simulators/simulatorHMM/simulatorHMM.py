from osbrain import Agent

from simulator import Simulator
from CT_simulators.simulatorHMM.DE_to_CT_wrapper import DeToCtWrapper


class SimulatorHMM(Simulator, Agent):
    """
    Specific simulator class for the HMM model
    """

    def __init__(self):
        super().__init__()
        self.wrapper = DeToCtWrapper()

    def run_state(self, state, data):
        """
        start execution of HMM model

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (dict)   model output data dictionary in the form
                                 {'output': [[0.43805922099522554, -0.5612743635978864], ...],
                                 'transformed input': [0.8062725477227317, ...]}
        """
        output = self.wrapper.run(data, state)
        return output
