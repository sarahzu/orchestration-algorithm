from simulatorE.simulatorE import SimulatorE
from simulator_factory import SimulatorFactory, handler_execution


class SimulatorEFactory(SimulatorFactory):

    def create_simulator(self):
        simulator = SimulatorE()
        return simulator


def handler_simulator(agent, message):
    simulatorE_factory = SimulatorEFactory()
    simulator_output_data = handler_execution(agent, message, simulatorE_factory.create_simulator())
    return simulator_output_data