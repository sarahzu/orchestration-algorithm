import json
from json import JSONDecodeError

from termcolor import colored

from simulator import Simulator


class SimulatorFactory:

    def create_simulator(self):
        simulator = Simulator()
        return simulator


def handler_simulator(agent, message):
    pass


def handler_execution(agent, message, simulator):
    """
    Agent handler function called whenever an agent uses the send() command. It runs the given simulator with the data
    extracted from the message.

    :param agent:       agent of the simulator
    :param message:     json string containing the run information for the simulator. In the form
                        {"time_step": 0, "data": [0,1,2,...]}
    :param simulator:   simulator which should run
    :return:            data output of simulator in the form [3,4,5,...]
    """
    try:
        input_json = json.loads(message)
        # set new computed data
        simulator_output_data = simulator.run_state(input_json["state"], input_json["data"])
        return simulator_output_data
    except JSONDecodeError:
        print(colored("------------\nwrong input format coming from " + str(agent) + "\ninput: "
                      + str(message) + "\nexpected input format: json\n------------", 'yellow'))
