from json.decoder import JSONDecodeError
from osbrain import run_nameserver, run_agent
from simulatorA.simulatorA import SimulatorA
from simulatorB.simulatorB import SimulatorB
from simulator import Simulator
import time
import json
import random
from termcolor import colored

initial_data = random.sample(range(10), 10)
max_time_step = 9
min_time_step = 0
curr_time_step = 0

simulatorA = SimulatorA("", curr_time_step, initial_data)
simulatorB = SimulatorB("", curr_time_step, initial_data)

# System deployment
ns = run_nameserver()
envA = run_agent('SimulatorA', attributes=dict(data=initial_data))
envB = run_agent('SimulatorB', attributes=dict(data=initial_data))


class Orchestrator:
    """
    Orchestrator responsible for linking simulators to agents and running them.
    """

    def __init__(self):

        self.time_step = curr_time_step
        self.data = initial_data
        print("Initial data: " + str(self.data))

    def run_simulation(self):
        """
        connect all simulators to an agent and let them run

        :return:
        """
        # Create a proxy to SimulatorA and log a message
        agent_simulatorA = ns.proxy('SimulatorA')
        agent_simulatorA.log_info('Hello world! Simulator A')

        # Create a proxy to SimulatorB and log a message
        agent_simulatorB = ns.proxy('SimulatorB')
        agent_simulatorB.log_info('Hello world! Simulator B')

        # System configuration:
        # connect agent of simulator A with agent of simulator B and vis versa
        addr_simulatorA = agent_simulatorA.bind('REP', alias='mainA', handler=handler_simulatorB)
        agent_simulatorB.connect(addr_simulatorA, alias='mainA')
        addr_simulatorB = agent_simulatorB.bind('REP', alias='mainB', handler=handler_simulatorA)
        agent_simulatorA.connect(addr_simulatorB, alias='mainB')

        # initial simulatorA output
        simulatorA_output = {
            "time_step": self.time_step,
            "data": self.data
        }

        while min_time_step <= self.time_step < max_time_step:
            # execute simulator B with output from simulator A
            simulatorB_output = self.execute_simulator_with_output_from_other_simulator(
                agent_simulatorB, simulatorA_output, 'mainA')
            print("SimulatorB output: " + str(simulatorB_output))

            # execute simulator A with output from simulator B
            simulatorA_output = self.execute_simulator_with_output_from_other_simulator(
                agent_simulatorA, simulatorB_output, 'mainB')
            self.time_step += 1
            print("SimulatorA output: " + str(simulatorA_output))

        ns.shutdown()

    def execute_simulator_with_output_from_other_simulator(self, agent_simulator_receiver, simulator_sender_input,
                                                           agent_sender_name):
        """
        Execute a receiver agent with input from a sender simulators agent

        :param agent_simulator_receiver:    simulator to be executed and which receives input
        :param simulator_sender_input:      input for receiving agent coming from the sending agent
        :param agent_sender_name:           name of sending agent
        :return:                            json containing the output data computed with executed simulator
        """
        agent_simulator_receiver.send(agent_sender_name, json.dumps(simulator_sender_input))
        simulator_receiver_output_data = agent_simulator_receiver.recv(agent_sender_name)

        simulator_receiver_output = {
            "time_step": self.time_step,
            "data": simulator_receiver_output_data
        }
        return simulator_receiver_output


def handler_simulatorA(agent, message):
    simulator_output_data = handler_execution(agent, message, simulatorA)
    return simulator_output_data


def handler_simulatorB(agent, message):
    simulator_output_data = handler_execution(agent, message, simulatorB)
    return simulator_output_data


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
        simulator_output_data = simulator.run_time_step(input_json["time_step"], input_json["data"])
        return simulator_output_data
    except JSONDecodeError:
        print(colored("------------\nwrong input format coming from " + str(agent) + "\ninput: "
              + str(message) + "\nexpected input format: json\n------------", 'yellow'))


if __name__ == '__main__':
    orchestrator = Orchestrator()
    orchestrator.run_simulation()
