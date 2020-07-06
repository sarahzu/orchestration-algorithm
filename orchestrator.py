import glob
import re
from json.decoder import JSONDecodeError
from os import listdir
from os.path import isfile, join

from osbrain import run_nameserver, run_agent
from simulatorA.simulatorA import SimulatorA
from simulatorB.simulatorB import SimulatorB
import json
import random
from termcolor import colored

from simulatorC.simulatorC import SimulatorC
from simulatorD.simulatorD import SimulatorD
from simulatorE.simulatorE import SimulatorE
from strategy.gauss_seidel_algorithm import GaussSeidelAlgorithm
from strategy.jacobi_algorithm import JacobiAlgorithm

initial_data = random.sample(range(10), 10)
max_state = 9
min_state = 0
curr_state = 0
communication_step = 1

simulatorA = SimulatorA(curr_state, initial_data)
simulatorB = SimulatorB(curr_state, initial_data)
simulatorC = SimulatorC(curr_state, initial_data)
simulatorD = SimulatorD(curr_state, initial_data)
simulatorE = SimulatorE(curr_state, initial_data)

# System deployment
ns = run_nameserver()

known_algorithms = ['Gauss-Seidel', 'Jacobi']


class Orchestrator:
    """
    Orchestrator responsible for linking simulators to agents and running them.
    """

    def __init__(self, algorithm):
        self.state = curr_state
        self.time_step = communication_step
        self.data = initial_data
        self.algorithm = algorithm
        print("Initial data: " + str(self.data))

    def extract_simulators(self):
        """
        extract all simulator files in the root folder

        :return:    list with all simulator filenames
        """
        simulator_list = []
        listing = glob.glob('simulator*')
        for filename in listing:
            try:
                files = [f for f in listdir(filename) if isfile(join(filename, f))]
                try:
                    files.remove('__init__.py')
                except ValueError:
                    pass
                regex = re.compile(r'model.\.py')
                filtered_files = [i for i in files if not regex.match(i)]
                simulator_list.extend(filtered_files)
            except NotADirectoryError:
                pass
        return simulator_list

    def connect_simulator_to_agent_proxy(self, simulator_names, simulator_index):
        """
        create agent proxy and connect it to the right simulator name

        :param simulator_names:     list of names of the simulators, e.g. ["simulatorA.py", ...]
        :param simulator_index:     index of the simulator in the simulator_names list which has to be connected
        :return:                    agent object of the corresponding simulator
        """
        simulator_name = simulator_names[simulator_index].strip('.py')
        run_agent(simulator_name)
        agent_simulator = ns.proxy(simulator_name)
        agent_simulator.log_info(simulator_name + ' connected')
        return agent_simulator

    def run_simulation(self):
        """
        connect all simulators to an agent and let them run

        :return:
        """

        # select all simulators
        simulator_names = sorted(self.extract_simulators())

        # choose the simulators to use, in this case simulator A (index 0) and B (index 1)
        agent_simulatorA = self.connect_simulator_to_agent_proxy(simulator_names, 0)
        agent_simulatorB = self.connect_simulator_to_agent_proxy(simulator_names, 1)
        agent_simulatorC = self.connect_simulator_to_agent_proxy(simulator_names, 2)

        # System configuration:
        # define connection adresses
        addr_simulatorA = agent_simulatorA.bind('REP', alias='mainA', handler=handler_simulatorB)
        addr_simulatorB = agent_simulatorB.bind('REP', alias='mainB', handler=handler_simulatorA)
        addr_simulatorC = agent_simulatorC.bind('REP', alias='mainC', handler=handler_simulatorC)
        # connect agents to receiving address
        agent_simulatorB.connect(addr_simulatorA, alias='mainA')
        agent_simulatorA.connect(addr_simulatorC, alias='mainC')
        agent_simulatorC.connect(addr_simulatorB, alias='mainB')

        # initial simulatorA output
        simulatorA_output = {
            "state": self.state,
            "data": self.data
        }

        # depending on used algorithm, execute different strategy
        simulator_object_list = [agent_simulatorB, agent_simulatorA, agent_simulatorC]
        simulator_name_list = ['mainA', 'mainC', 'mainB']
        # simulator_order = {0: agent_simulatorB, 1: agent_simulatorA}
        if self.algorithm.lower() == 'gauss-seidel':
            # run gauss seidel algorithm
            gauss_seidel_algorithm = GaussSeidelAlgorithm()
            final_state, final_data = gauss_seidel_algorithm.algorithm(
                min_state, self.state, max_state, simulator_object_list, simulator_name_list,
                simulatorA_output, self.time_step)

            print("final state: " + str(final_state) + "\nfinal data: " + str(final_data['data']))

        elif self.algorithm.lower() == 'jacobi':
            pass
            # run jacobi algorithm
            jacobi_algorithm = JacobiAlgorithm()
            final_state, final_data = jacobi_algorithm.algorithm(
                min_state, self.state, max_state, simulator_object_list, simulator_name_list,
                simulatorA_output, self.time_step)

            print("final time step: " + str(final_state) + "\nfinal data: " + str(final_data['data']))
        else:
            print(colored("------------\nalgorithm \"" + str(self.algorithm) +
                          "\" given to orchestrator is not known.\nplease select one of the following algorithms: "
                          + str(known_algorithms) + "\n------------", 'yellow'))
        ns.shutdown()


def handler_simulatorA(agent, message):
    simulator_output_data = handler_execution(agent, message, simulatorA)
    return simulator_output_data


def handler_simulatorB(agent, message):
    simulator_output_data = handler_execution(agent, message, simulatorB)
    return simulator_output_data


def handler_simulatorC(agent, message):
    simulator_output_data = handler_execution(agent, message, simulatorC)
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
        simulator_output_data = simulator.run_time_step(input_json["state"], input_json["data"])
        return simulator_output_data
    except JSONDecodeError:
        print(colored("------------\nwrong input format coming from " + str(agent) + "\ninput: "
                      + str(message) + "\nexpected input format: json\n------------", 'yellow'))


if __name__ == '__main__':
    jacobi = 'jacobi'
    gauss = 'gauss-seidel'
    orchestrator = Orchestrator(gauss)
    orchestrator.run_simulation()
