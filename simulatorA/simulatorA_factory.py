from simulatorA.simulatorA import SimulatorA
from simulator_factory import handler_execution

simulator = SimulatorA()


def handler_simulator(agent, message):
    simulator_output_data = handler_execution(agent, message, simulator)
    return simulator_output_data
