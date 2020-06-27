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
max_time_step = 99
min_time_step = 0
curr_time_step = 0

simulatorA = SimulatorA("", curr_time_step, initial_data)
simulatorB = SimulatorB("", curr_time_step, initial_data)

# System deployment
ns = run_nameserver()
envA = run_agent('SimulatorA', attributes=dict(data=initial_data))
envB = run_agent('SimulatorB', attributes=dict(data=initial_data))


class Orchestrator:

    def __init__(self):

        self.time_step = curr_time_step
        self.data = initial_data
        print("Initial data: " + str(self.data))

    def run_simulation(self):
        # Create a proxy to SimulatorA and log a message
        agent_simulatorA = ns.proxy('SimulatorA')
        agent_simulatorA.log_info('Hello world! Simulator A')

        # Create a proxy to SimulatorB and log a message
        agent_simulatorB = ns.proxy('SimulatorB')
        agent_simulatorB.log_info('Hello world! Simulator B')

        # System configuration
        addr_simulatorA = agent_simulatorA.bind('REP', alias='mainA', handler=handler_simulatorB)
        agent_simulatorB.connect(addr_simulatorA, alias='mainA')
        addr_simulatorB = agent_simulatorB.bind('REP', alias='mainB', handler=handler_simulatorA)
        agent_simulatorA.connect(addr_simulatorB, alias='mainB')

        # execute simulator B with input from simulator A
        simulatorA_input = {
            "time_step": self.time_step,
            "data": self.data
        }
        agent_simulatorB.send("mainA", json.dumps(simulatorA_input))
        self.time_step += 1
        simulatorB_input_data = agent_simulatorB.recv('mainA')
        print("simulator B input data: " + str(simulatorB_input_data))

        # execute simulator A with input from simulator B
        simulatorB_input = {
            "time_step": self.time_step,
            "data": simulatorB_input_data
        }
        agent_simulatorA.send("mainB", json.dumps(simulatorB_input))
        self.time_step += 1
        simulatorA_input_data = agent_simulatorA.recv('mainB')
        print("simulator A input data: " + str(simulatorA_input_data))

        ns.shutdown()


def handler_simulatorA(agent, message):
    try:
        input_json = json.loads(message)
        # set new computed data
        new_output_data = simulatorA.run_time_step(input_json["time_step"], input_json["data"])
        return new_output_data
    except JSONDecodeError:
        print(colored("------------\nwrong input format coming from " + str(agent) + "\ninput: "
              + str(message) + "\nexpected input format: json\n------------", 'yellow'))


def handler_simulatorB(agent, message):
    try:
        input_json = json.loads(message)
        # set new computed data
        new_output_data = simulatorB.run_time_step(input_json["time_step"], input_json["data"])
        return new_output_data
    except JSONDecodeError:
        print(colored("------------\nwrong input format coming from " + str(agent) + "\ninput: "
              + str(message) + "\nexpected input format: json\n------------", 'yellow'))


if __name__ == '__main__':
    orchestrator = Orchestrator()
    orchestrator.run_simulation()
