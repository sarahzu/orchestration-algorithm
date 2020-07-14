import glob
import re
from os import listdir
from os.path import isfile, join
from osbrain import run_nameserver, run_agent
from simulatorA import simulatorA_factory
from simulatorB import simulatorB_factory
import random
from termcolor import colored
from simulatorC import simulatorC_factory
from simulatorD import simulatorD_factory
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

    def __init__(self, algorithm, simulator_list, initial_data_dict):
        self.state = curr_state
        self.time_step = communication_step
        #self.data = initial_data
        self.algorithm = algorithm
        #print("Initial data: " + str(self.data))
        self.simulator_list = simulator_list
        self.dependencies = {}
        self.initial_data_dict = initial_data_dict

    def run_simulation(self):
        """
        connect all simulators to an agent and let them run

        :return:
        """

        # connect all simulators to agents and store agent in simulator_list
        simulator_list_in_correct_order = [0] * len(simulator_list)
        alias_list_in_correct_order = [0] * len(simulator_list)
        simulator_initial_inputs = {}
        for simulator_dict in self.simulator_list:
            agent_simulator = connect_simulator_to_agent_proxy(simulator_dict["name"])
            # store newly defined agent in corresponding simulator_list entry
            simulator_dict['agent'] = agent_simulator
            simulator_initial_inputs[simulator_dict["name"]] = {
                "state": self.state,
                "data": self.initial_data_dict[simulator_dict["name"]]
            }
            self.dependencies[simulator_dict["name"]] = simulator_dict["dependency"]

        # System configuration:
        # define connection addresses
        for simulator_dict in self.simulator_list:
            connection_alias = simulator_dict["name"]
            # define agent connection address
            addr_simulator = simulator_dict["agent"].bind('REP', alias=connection_alias,
                                                          handler=simulator_dict["factory"].handler_simulator)
            # creat simulator order dict and place alias at corresponding order index
            alias_list_in_correct_order[simulator_dict["order"]] = connection_alias

            # connect next simulator to address of current simulator
            if simulator_dict["order"] != len(self.simulator_list) - 1:
                next_simulator_order = simulator_dict["order"] + 1
            else:
                next_simulator_order = 0
            for simulator_dict_next in self.simulator_list:
                # check if next simulator is in current simulators next list
                if simulator_dict_next["order"] == next_simulator_order:
                    simulator_dict_next["agent"].connect(addr_simulator, alias=connection_alias)
                    # put connected simulator in simulator order list at its corresponding order index
                    simulator_list_in_correct_order[simulator_dict["order"]] = simulator_dict_next["agent"]

        # depending on used algorithm, execute different strategy
        state_history = {self.state: simulator_initial_inputs}
        if self.algorithm.lower() == 'gauss-seidel':
            # run gauss seidel algorithm
            gauss_seidel_algorithm = GaussSeidelAlgorithm()
            final_state, final_data = gauss_seidel_algorithm.algorithm(
                min_state, self.state, max_state, simulator_list_in_correct_order, alias_list_in_correct_order,
                simulator_initial_inputs, self.time_step, self.dependencies, state_history)

            print("final state: " + str(final_state) + "\nfinal data: " + str(final_data))

        elif self.algorithm.lower() == 'jacobi':
            # run jacobi algorithm
            jacobi_algorithm = JacobiAlgorithm()
            final_state, final_data = jacobi_algorithm.algorithm(
                min_state, self.state, max_state, simulator_list_in_correct_order, alias_list_in_correct_order,
                simulator_initial_inputs, self.time_step, self.dependencies, state_history)

            print("final time step: " + str(final_state) + "\nfinal data: " + str(final_data))
        else:
            print(colored("------------\nalgorithm \"" + str(self.algorithm) +
                          "\" given to orchestrator is not known.\nplease select one of the following algorithms: "
                          + str(known_algorithms) + "\n------------", 'yellow'))
        ns.shutdown()


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

    simulator_list = [{"name": "simulatorA", "factory": simulatorB_factory,
                       "dependency": ["simulatorB", "simulatorC"], "order": 1},
                      {"name": "simulatorB", "factory": simulatorA_factory,
                       "dependency": ["simulatorC", "simulatorA"], "order": 3}, #2},
                      {"name": "simulatorC", "factory": simulatorC_factory,
                       "dependency": ["simulatorB"], "order": 0}, #]
                      {"name": "simulatorD", "factory": simulatorD_factory,
                       "dependency": ["simulatorB", "simulatorA"], "order": 2}]

    initial_data_dict = {"simulatorA": [1, 2], "simulatorB": [5, 6], "simulatorC": [9, 16], "simulatorD": [18, 21]}

    jacobi = 'jacobi'
    gauss = 'gauss-seidel'
    orchestrator = Orchestrator(jacobi, simulator_list, initial_data_dict)
    orchestrator.run_simulation()
