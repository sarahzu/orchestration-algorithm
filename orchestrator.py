import glob
import json
import re
from os import listdir
from os.path import isfile, join
from osbrain import run_nameserver, run_agent
from simulatorA import simulatorA_factory
from simulatorB import simulatorB_factory
import random
from termcolor import colored
from simulatorC import simulatorC_factory
from DE_simulators.simulatorCiw import simulatorCiw_factory
from simulatorD import simulatorD_factory
from simulatorE import simulatorE_factory
from CT_Simulators.simulatorHMM import simulatorHMM_factory
from strategy.gauss_seidel_algorithm import GaussSeidelAlgorithm
from strategy.jacobi_algorithm import JacobiAlgorithm
import jsbeautifier

initial_data = random.sample(range(10), 10)
max_state = 9
min_state = 0
curr_state = 0
communication_step = 1

known_algorithms = ['Gauss-Seidel', 'Jacobi']


def connect_simulator_to_agent_proxy(simulator_name):
    """
    create agent proxy and connect it to the right simulator name

    :param simulator_name:      (string) name of simulator
    :return:                    (agent)  agent object of the corresponding simulator
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

    def __init__(self, algorithm, simulator_information_list, initial_simulator_input_data_dict):
        self.state = curr_state
        self.time_step = communication_step
        # self.data = initial_data
        self.used_algorithm = algorithm
        # print("Initial data: " + str(self.data))
        self.simulator_information_list = simulator_information_list
        self.dependencies = {}
        self.initial_simulator_input_data_dict = initial_simulator_input_data_dict

    def run_simulation(self):
        """
        connect all simulators to an agent and let them run

        :return:
        """

        # connect all simulators to agents and store agent in simulator_list
        simulator_list_in_correct_order = [0] * len(self.simulator_information_list)
        alias_list_in_correct_order = [0] * len(self.simulator_information_list)

        simulator_initial_inputs = {}
        for simulator_dict in self.simulator_information_list:
            agent_simulator = connect_simulator_to_agent_proxy(simulator_dict["name"])
            # store newly defined agent in corresponding simulator_list entry
            simulator_dict['agent'] = agent_simulator
            simulator_initial_inputs[simulator_dict["name"]] = {
                "state": self.state,
                "data": self.initial_simulator_input_data_dict[simulator_dict["name"]]
            }
            self.dependencies[simulator_dict["name"]] = simulator_dict["dependency"]

        # System configuration:
        # define connection addresses
        for simulator_dict in self.simulator_information_list:
            connection_alias = simulator_dict["name"]
            # define agent connection address
            addr_simulator = simulator_dict["agent"].bind('REP', alias=connection_alias,
                                                          handler=simulator_dict["factory"].handler_simulator)
            # creat simulator order dict and place alias at corresponding order index
            alias_list_in_correct_order[simulator_dict["order"]] = connection_alias

            # connect next simulator to address of current simulator
            if simulator_dict["order"] != len(self.simulator_information_list) - 1:
                next_simulator_order = simulator_dict["order"] + 1
            else:
                next_simulator_order = 0
            for simulator_dict_next in self.simulator_information_list:
                # check if next simulator is in current simulators next list
                if simulator_dict_next["order"] == next_simulator_order:
                    simulator_dict_next["agent"].connect(addr_simulator, alias=connection_alias)
                    # put connected simulator in simulator order list at its corresponding order index
                    simulator_list_in_correct_order[simulator_dict["order"]] = simulator_dict_next["agent"]

        # depending on used used_algorithm, execute different strategy
        state_history = {self.state: simulator_initial_inputs}
        if self.used_algorithm.lower() == 'gauss-seidel':
            # run gauss seidel used_algorithm
            gauss_seidel_algorithm = GaussSeidelAlgorithm()
            final_state, final_data = gauss_seidel_algorithm.algorithm(
                min_state, self.state, max_state, simulator_list_in_correct_order, alias_list_in_correct_order,
                simulator_initial_inputs, self.time_step, self.dependencies, state_history)

        elif self.used_algorithm.lower() == 'jacobi':
            # run jacobi used_algorithm
            jacobi_algorithm = JacobiAlgorithm()
            final_state, final_data = jacobi_algorithm.algorithm(
                min_state, self.state, max_state, simulator_list_in_correct_order, alias_list_in_correct_order,
                simulator_initial_inputs, self.time_step, self.dependencies, state_history)
        else:
            print(colored("------------\nused_algorithm \"" + str(self.used_algorithm) +
                          "\" given to orchestrator is not known.\nplease select one of the following algorithms: "
                          + str(known_algorithms) + "\n------------", 'yellow'))
            ns.shutdown()
            return None

        ns.shutdown()

        json_parse_options = jsbeautifier.default_options()
        json_parse_options.indent_size = 4
        formatted_final_data = jsbeautifier.beautify(json.dumps(final_data), json_parse_options)
        print("output state: " + str(final_state) +
              "\noutput data: " + formatted_final_data)

        with open("simulation_output.json", "w") as outfile:
            outfile.write(formatted_final_data)


def extract_simulators():
    """
    extract all simulator files in the root folder

    :return:    (list) list with all simulator filenames
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

    simulator_list = [{"name": "simulatorA", "factory": simulatorA_factory,
                       "dependency": ["simulatorB", "simulatorC"], "order": 1},
                      {"name": "simulatorB", "factory": simulatorB_factory,
                       "dependency": ["simulatorC", "simulatorA"], "order": 3},  # 2},
                      {"name": "simulatorC", "factory": simulatorC_factory,
                       "dependency": ["simulatorB"], "order": 0},  # ]
                      {"name": "simulatorD", "factory": simulatorD_factory,
                       "dependency": ["simulatorB", "simulatorA"], "order": 2}]

    simulator_list_gauss = [{"name": "simulatorC", "factory": simulatorC_factory,
                             "dependency": ["simulatorE"], "order": 0},
                            {"name": "simulatorE", "factory": simulatorE_factory,
                             "dependency": ["simulatorC"], "order": 1}]

    simulator_list_hybrid = [{"name": "simulatorHMM", "factory": simulatorHMM_factory,
                            "dependency": ["simulatorCiw"], "order": 0},
                             {"name": "simulatorCiw", "factory": simulatorCiw_factory,
                            "dependency": ["simulatorHMM"], "order": 1}]

    initial_data_dict = {"simulatorA": [1, 2], "simulatorB": [5, 6], "simulatorC": [9, 18], "simulatorD": [18, 21]}

    initial_data_dict_gauss = {"simulatorC": [9, 18], "simulatorE": [8, 19]}

    initial_data_dict_test_hybrid = {"simulatorHMM": [2.561081835113113, 4.20021128824225862, -1.288692891201176, 8.717137161312187, 2.429789708506107], "simulatorCiw": [0.20627254772273172]}

    # print("s: " + str(StrategyAlgorithm().extrapolate2([5, 6], [[1, 2], [1, 3]], 2)))

    jacobi = 'jacobi'
    gauss = 'gauss-seidel'
    # orchestrator = Orchestrator(gauss, simulator_list_gauss, initial_data_dict_gauss)
    # orchestrator = Orchestrator(jacobi, simulator_list, initial_data_dict)
    # orchestrator = Orchestrator(jacobi, simulator_list_test, initial_data_dict_test)
    orchestrator = Orchestrator(jacobi, simulator_list_hybrid, initial_data_dict_test_hybrid)

    orchestrator.run_simulation()
