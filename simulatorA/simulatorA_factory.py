from simulatorA.simulatorA import SimulatorA
from simulator_factory import SimulatorFactory, handler_execution


class SimulatorAFactory(SimulatorFactory):

    def create_simulator(self):
        simulator = SimulatorA()
        return simulator


def handler_simulator(agent, message):
    simulatorA_factory = SimulatorAFactory()
    simulator_output_data = handler_execution(agent, message, simulatorA_factory.create_simulator())
    return simulator_output_data
