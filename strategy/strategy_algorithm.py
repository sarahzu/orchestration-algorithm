import json


class StrategyAlgorithm:

    def __init__(self):
        pass

    def algorithm(self, min_state, state, max_state, agent_simulator_object_list, agent_simulator_name_list,
                  initial_input, time_step):
        pass

    def execute_simulator_with_output_from_other_simulator(self, agent_simulator_receiver, simulator_sender_input,
                                                           agent_sender_name, state):
        """
        Execute a receiver agent with input from a sender simulators agent

        :param agent_simulator_receiver:    simulator to be executed and which receives input
        :param simulator_sender_input:      input for receiving agent coming from the sending agent
        :param agent_sender_name:           name of sending agent
        :param state:                       current time state
        :return:                            json containing the output data computed with executed simulator
        """
        agent_simulator_receiver.send(agent_sender_name, json.dumps(simulator_sender_input))
        simulator_receiver_output_data = agent_simulator_receiver.recv(agent_sender_name)

        simulator_receiver_output = {
            "state": state,
            "data": simulator_receiver_output_data
        }
        return simulator_receiver_output
