from osbrain import Agent

from simulator import Simulator


class DESimulator(Simulator, Agent):

    def __init__(self):
        super().__init__()

    def run_state(self, state, data):
        pass
