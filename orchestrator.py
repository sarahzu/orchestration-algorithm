from simulatorA import simulatorA
from simulatorB import simulatorB


class Orchestrator:

    def __init__(self):
        self.simulatorA = simulatorA.SimulatorA()
        self.simulatorB = simulatorB.SimulatorB()
