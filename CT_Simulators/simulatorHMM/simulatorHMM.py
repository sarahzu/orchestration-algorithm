from osbrain import Agent

from simulator import Simulator
from CT_Simulators.simulatorHMM.DE_to_CT_wrapper import DeToCtWrapper


class SimulatorHMM(Simulator, Agent):
    """
    Specific simulator class for the model D
    """

    def __init__(self):
        super().__init__()
        self.wrapper = DeToCtWrapper()

    def run_state(self, state, data):
        """
        start execution of model D

        :param state:   (string) current state
        :param data:    (list)   input data list used to run the model
        :return:        (list)   model output data list
        """
        output = self.wrapper.run(data, state)
        return output
