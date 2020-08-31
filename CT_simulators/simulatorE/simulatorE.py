from osbrain import Agent
from CT_simulators.simulatorE.e_wrapper import EWrapper
from simulator import Simulator


class SimulatorE(Simulator, Agent):
    """
    Specific simulator class for the model E
    """

    def __init__(self):
        super().__init__()
        self.wrapper = EWrapper()

    def run_state(self, state, data):
        """
        start execution of model E

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (dict)   model output data dictionary in the form
                                 {'output': [-36, 5], 'transformed input': [-2, 19]}
        """
        output = self.wrapper.run(data, state)
        return output

