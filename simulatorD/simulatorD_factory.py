from simulatorD.simulatorD import SimulatorD
from simulator_factory import SimulatorFactory, handler_execution


class SimulatorDFactory(SimulatorFactory):

    def create_simulator(self):
        simulator = SimulatorD()
        return simulator


def handler_simulator(agent, message):
    simulatorD_factory = SimulatorDFactory()
    simulator_output_data = handler_execution(agent, message, simulatorD_factory.create_simulator())
    return simulator_output_data
