from simulatorD.simulatorD import SimulatorD
from simulator_factory import handler_execution


simulator = SimulatorD()


def handler_simulator(agent, message):
    simulator_output_data = handler_execution(agent, message, simulator)
    return simulator_output_data
