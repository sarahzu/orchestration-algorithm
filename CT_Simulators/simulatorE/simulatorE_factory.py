from CT_Simulators.simulatorE.simulatorE import SimulatorE
from simulator_factory import handler_execution

simulator = SimulatorE()


def handler_simulator(agent, message):
    """
    handler function used by the agents to run a simulator and return its output data

    :param agent:       (agent)  agent connected to the simulator
    :param message:     (string) message containing the input data of the simulator
    :return:            (list)   simulator's output data
    """
    simulator_output_data = handler_execution(agent, message, simulator)
    return simulator_output_data
