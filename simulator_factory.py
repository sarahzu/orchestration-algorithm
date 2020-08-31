import json
from json import JSONDecodeError

from termcolor import colored


def handler_execution(agent, message, simulator):
    """
    Agent handler function called whenever an agent uses the send() command. It runs the given simulator with the data
    extracted from the message.

    :param agent:       (agent)     agent of the simulator
    :param message:     (string)    json string containing the run information for the simulator,
                                    in the form: {"state": 0, "data": [0,1,2,...]}
    :param simulator:   (Simulator) simulator object which should be run
    :return:            (list)      data output of simulator in the form [3,4,5,...]
    """
    try:
        input_json = json.loads(message)
        simulator_output_data = simulator.run_state(input_json["state"], input_json["output data"])
        return simulator_output_data
    except JSONDecodeError:
        print(colored("------------\nwrong input format coming from " + str(agent) + "\ninput: "
                      + str(message) + "\nexpected input format: string\n------------", 'yellow'))
        return []
