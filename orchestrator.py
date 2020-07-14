import collections
import glob
import re
from json.decoder import JSONDecodeError
from os import listdir
from os.path import isfile, join

from osbrain import run_nameserver, run_agent

from simulatorA import simulatorA_factory
from simulatorA.simulatorA import SimulatorA
from simulatorA.simulatorA_factory import SimulatorAFactory
from simulatorB import simulatorB_factory
from simulatorB.simulatorB import SimulatorB
import json
import random
from termcolor import colored

from simulatorB.simulatorB_factory import SimulatorBFactory
from simulatorC import simulatorC_factory
from simulatorC.simulatorC import SimulatorC
from simulatorC.simulatorC_factory import SimulatorCFactory
from simulatorD import simulatorD_factory
from simulatorD.simulatorD import SimulatorD
from simulatorD.simulatorD_factory import SimulatorDFactory
from simulatorE.simulatorE import SimulatorE
from simulatorE.simulatorE_factory import SimulatorEFactory
from strategy.gauss_seidel_algorithm import GaussSeidelAlgorithm
from strategy.jacobi_algorithm import JacobiAlgorithm

initial_data = random.sample(range(10), 10)
max_state = 9
min_state = 0
curr_state = 0
communication_step = 1

known_algorithms = ['Gauss-Seidel', 'Jacobi']


def connect_simulator_to_agent_proxy(simulator_name):
    """
    create agent proxy and connect it to the right simulator name

    :param simulator_name:      name of simulator
    :return:                    agent object of the corresponding simulator
    """
    # simulator_name = simulator_name.strip('.py')
    run_agent(simulator_name)
    agent_simulator = ns.proxy(simulator_name)
    agent_simulator.log_info(simulator_name + ' connected')
    return agent_simulator


class Orchestrator:
    """
    Orchestrator responsible for linking simulators to agents and running them.
    """

    def __init__(self, algorithm, simulator_list):
        self.state = curr_state
        self.time_step = communication_step
        self.data = initial_data
        self.algorithm = algorithm
        print("Initial data: " + str(self.data))
        self.simulator_list = simulator_list
        self.dependencies = {}

    def run_simulation(self):
        """
        connect all simulators to an agent and let them run

        :return:
        """

        # initial simulatorA output
        initial_simulator_input = {
            "state": self.state,
            "data": self.data
        }

        # connect all simulators to agents and store agent in simulator_list
        simulator_order = [0] * len(simulator_list)
        alias_order = [0] * len(simulator_list)
        simulator_outputs = {}
        for simulator_dict in self.simulator_list:
            agent_simulator = connect_simulator_to_agent_proxy(simulator_dict["name"])
            # store newly defined agent in corresponding simulator_list entry
            simulator_dict['agent'] = agent_simulator
            simulator_outputs[simulator_dict["name"]] = initial_simulator_input
            self.dependencies[simulator_dict["name"]] = simulator_dict["dependency"]

        # System configuration:
        # define connection addresses
        # simulator_name_list = ['mainA', 'mainC', 'mainB']
        # simulator_object_list = [agent_simulatorB, agent_simulatorA, agent_simulatorC]
        # simulator_object_list = []
        # simulator_alias_name_list = []
        for simulator_dict in self.simulator_list:
            connection_alias = simulator_dict["name"]
            # define agent connection address
            addr_simulator = simulator_dict["agent"].bind('REP', alias=connection_alias,
                                                          handler=simulator_dict["factory"].handler_simulator)
            # creat simulator order dict and place alias at corresponding order index
            alias_order[simulator_dict["order"]] = connection_alias

            # connect next simulator to address of current simulator
            for simulator_dict_next in self.simulator_list:
                # check if next simulator is in current simulators next list
                if simulator_dict_next["name"] == simulator_dict["next simulator"]:
                    simulator_dict_next["agent"].connect(addr_simulator, alias=connection_alias)
                    # simulator_alias_name_list.append(connection_alias)
                    # simulator_object_list.append(simulator_dict_next["agent"])

                    # put connected simulator in simulator order list at its corresponding order index
                    simulator_order[simulator_dict["order"]] = simulator_dict_next["agent"]

        # addr_simulatorA = agent_simulatorA.bind('REP', alias='mainA', handler=simulatorB_factory.handler_simulator)
        # addr_simulatorB = agent_simulatorB.bind('REP', alias='mainB', handler=simulatorA_factory.handler_simulator)
        # addr_simulatorC = agent_simulatorC.bind('REP', alias='mainC', handler=simulatorC_factory.handler_simulator)
        # connect agents to receiving address

        # # B runs with input from A (address)
        # agent_simulatorB.connect(addr_simulatorA, alias='mainA')
        # # A runs with input from C (address)
        # agent_simulatorA.connect(addr_simulatorC, alias='mainC')
        # # C runs with input from B (address)
        # agent_simulatorC.connect(addr_simulatorB, alias='mainB')

        # simulator_inputs = {}
        # for key, value in dependencies.items():
        #     simulator_inputs[key] = []
        #     for dependency in value:
        #         simulator_inputs[key].append(self.data)


        # depending on used algorithm, execute different strategy
        # simulator_order = {0: agent_simulatorB, 1: agent_simulatorA}
        state_history = {self.state: simulator_outputs}
        if self.algorithm.lower() == 'gauss-seidel':
            # run gauss seidel algorithm
            gauss_seidel_algorithm = GaussSeidelAlgorithm()
            print(str(initial_simulator_input))
            final_state, final_data = gauss_seidel_algorithm.algorithm(
                min_state, self.state, max_state, simulator_order, alias_order,
                # initial_simulator_input, self.time_step, self.dependencies)
                simulator_outputs, self.time_step, self.dependencies, state_history)

            print("final state: " + str(final_state) + "\nfinal data: " + str(final_data))

        elif self.algorithm.lower() == 'jacobi':
            # run jacobi algorithm
            jacobi_algorithm = JacobiAlgorithm()
            final_state, final_data = jacobi_algorithm.algorithm(
                min_state, self.state, max_state, simulator_order, alias_order,
                simulator_outputs, self.time_step, self.dependencies, state_history)

            print("final time step: " + str(final_state) + "\nfinal data: " + str(final_data))
        else:
            print(colored("------------\nalgorithm \"" + str(self.algorithm) +
                          "\" given to orchestrator is not known.\nplease select one of the following algorithms: "
                          + str(known_algorithms) + "\n------------", 'yellow'))
        ns.shutdown()


# def handler_simulatorA(agent, message):
#     simulator_output_data = handler_execution(agent, message, simulatorA)
#     return simulator_output_data
#
#
# def handler_simulatorB(agent, message):
#     simulator_output_data = handler_execution(agent, message, simulatorB)
#     return simulator_output_data
#
#
# def handler_simulatorC(agent, message):
#     simulator_output_data = handler_execution(agent, message, simulatorC)
#     return simulator_output_data
#
#
# def handler_execution(agent, message, simulator):
#     """
#     Agent handler function called whenever an agent uses the send() command. It runs the given simulator with the data
#     extracted from the message.
#
#     :param agent:       agent of the simulator
#     :param message:     json string containing the run information for the simulator. In the form
#                         {"time_step": 0, "data": [0,1,2,...]}
#     :param simulator:   simulator which should run
#     :return:            data output of simulator in the form [3,4,5,...]
#     """
#     try:
#         input_json = json.loads(message)
#         # set new computed data
#         simulator_output_data = simulator.run_state(input_json["state"], input_json["data"])
#         return simulator_output_data
#     except JSONDecodeError:
#         print(colored("------------\nwrong input format coming from " + str(agent) + "\ninput: "
#                       + str(message) + "\nexpected input format: json\n------------", 'yellow'))


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


def extract_simulators():
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


if __name__ == '__main__':
    # System deployment
    ns = run_nameserver()

    simulator_list = [{"name": "simulatorA", "factory": simulatorB_factory, "next simulator": "simulatorD", # "simulatorB",
                       "dependency": ["simulatorB", "simulatorC"], "order": 1},
                      {"name": "simulatorB", "factory": simulatorA_factory, "next simulator": "simulatorC",
                       "dependency": ["simulatorC", "simulatorA"], "order": 3},#2},
                      {"name": "simulatorC", "factory": simulatorC_factory, "next simulator": "simulatorA",
                       "dependency": ["simulatorB"], "order": 0}, #]
                      {"name": "simulatorD", "factory": simulatorD_factory, "next simulator": "simulatorB",
                       "dependency": ["simulatorB", "simulatorA"], "order": 2}]

    jacobi = 'jacobi'
    gauss = 'gauss-seidel'
    orchestrator = Orchestrator(jacobi, simulator_list)
    orchestrator.run_simulation()
