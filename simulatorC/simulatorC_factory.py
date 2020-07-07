from simulatorC.simulatorC import SimulatorC
from simulator_factory import SimulatorFactory, handler_execution


class SimulatorCFactory(SimulatorFactory):

    def create_simulator(self):
        simulator = SimulatorC()
        return simulator


def handler_simulator(agent, message):
    simulatorC_factory = SimulatorCFactory()
    simulator_output_data = handler_execution(agent, message, simulatorC_factory.create_simulator())
    return simulator_output_data
