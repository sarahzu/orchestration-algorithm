from simulatorB.simulatorB import SimulatorB
from simulator_factory import SimulatorFactory, handler_execution


class SimulatorBFactory(SimulatorFactory):

    def create_simulator(self):
        simulator = SimulatorB()
        return simulator


def handler_simulator(agent, message):
    simulatorB_factory = SimulatorBFactory()
    simulator_output_data = handler_execution(agent, message, simulatorB_factory.create_simulator())
    return simulator_output_data
