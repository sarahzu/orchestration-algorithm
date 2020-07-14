from simulatorC.simulatorC import SimulatorC
from simulator_factory import handler_execution


simulator = SimulatorC()


def handler_simulator(agent, message):
    simulator_output_data = handler_execution(agent, message, simulator)
    return simulator_output_data
