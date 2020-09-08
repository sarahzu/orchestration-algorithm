import json
import jsbeautifier

from osbrain import run_nameserver, run_agent
from termcolor import colored
from CT_simulators.simulatorE import simulatorE_factory
from CT_simulators.simulatorLG import simulatorLG_factory
from DE_simulators.simulatorA import simulatorA_factory
from CT_simulators.simulatorB import simulatorB_factory
from DE_simulators.simulatorC import simulatorC_factory
from DE_simulators.simulatorCiw import simulatorCiw_factory
from CT_simulators.simulatorD import simulatorD_factory
from CT_simulators.simulatorHMM import simulatorHMM_factory
from strategy.gauss_seidel_algorithm import GaussSeidelAlgorithm
from strategy.jacobi_algorithm import JacobiAlgorithm

max_state = 9
min_state = 0
curr_state = 0
communication_step = 1

known_coupling_algorithms = ['Gauss-Seidel', 'Jacobi']


class Orchestrator:
    """
    Orchestrator responsible for linking simulators to agents and running them by using a simulation coupling algorithm
    """

    def __init__(self, coupling_algorithm, simulator_information_list, initial_simulator_input_data_dict):
        """

        :param coupling_algorithm:                  (string) name of the used coupling algorithm
        :param simulator_information_list:          (list)   list of every simulators initial information
                                                             in form of a dictionary:
                                                             e.g. [
                                                                    {
                                                                        'name': 'simulatorC',
                                                                        'factory': simulatorCFactoryObject,
                                                                        'dependency': ['simulatorE'],
                                                                        'order': 0
                                                                    },
                                                                    {...},
                                                                    ...
                                                                  ]
        :param initial_simulator_input_data_dict:   (dict)  dictionary containing for each simulator its corresponding
                                                            initial data list:
                                                            e.g. {'simulatorC': [6], 'simulatorE': [8, 19]}
        """
        self.state = curr_state
        self.time_step = communication_step
        self.used_coupling_algorithm = coupling_algorithm
        self.simulator_information_list = simulator_information_list
        self.dependencies = {}
        self.initial_simulator_input_data_dict = initial_simulator_input_data_dict

    def run_simulation(self):
        """
        connect all simulators to an agent and let them run their connected simulators

        :return:
        """
        # define empty lists for ordered simulators and their corresponding agent aliases
        simulator_list_in_correct_order = [0] * len(self.simulator_information_list)
        alias_list_in_correct_order = [0] * len(self.simulator_information_list)

        # connect all simulators to agents and store agent in simulator list
        simulator_initial_inputs = {}
        for simulator_dict in self.simulator_information_list:
            agent_simulator = connect_simulator_to_agent_proxy(simulator_dict["name"])
            # store newly defined agent in corresponding simulator list entry
            simulator_dict['agent'] = agent_simulator
            simulator_initial_inputs[simulator_dict["name"]] = {
                "output data": self.initial_simulator_input_data_dict[simulator_dict["name"]]
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

            # define order of next simulator
            if simulator_dict["order"] != len(self.simulator_information_list) - 1:
                next_simulator_order = simulator_dict["order"] + 1
            else:
                next_simulator_order = 0

            # connect next simulator to address of current simulator
            for simulator_dict_next in self.simulator_information_list:
                # check if next simulator is in current simulators next list
                if simulator_dict_next["order"] == next_simulator_order:
                    simulator_dict_next["agent"].connect(addr_simulator, alias=connection_alias)
                    # put connected simulator in simulator order list at its corresponding order index
                    simulator_list_in_correct_order[simulator_dict["order"]] = simulator_dict_next["agent"]

        state_history = {self.state: simulator_initial_inputs}

        # depending on used coupling algorithm, execute different strategy
        if self.used_coupling_algorithm.lower() == 'gauss-seidel':
            # run gauss-seidel coupling algorithm
            gauss_seidel_coupling_algorithm = GaussSeidelAlgorithm()
            final_state, final_data = gauss_seidel_coupling_algorithm.algorithm(
                min_state, self.state, max_state, simulator_list_in_correct_order, alias_list_in_correct_order,
                simulator_initial_inputs, self.time_step, self.dependencies, state_history)

        elif self.used_coupling_algorithm.lower() == 'jacobi':
            # run jacobi coupling algorithm
            jacobi_coupling_algorithm = JacobiAlgorithm()
            final_state, final_data = jacobi_coupling_algorithm.algorithm(
                min_state, self.state, max_state, simulator_list_in_correct_order, alias_list_in_correct_order,
                simulator_initial_inputs, self.time_step, self.dependencies, state_history)
        else:
            print(colored("------------\ncoupling algorithm \"" + str(self.used_coupling_algorithm) +
                          "\" given to orchestrator is not known."
                          "\nplease select one of the following coupling algorithms: "
                          + str(known_coupling_algorithms) + "\n------------", 'yellow'))
            ns.shutdown()
            return None

        ns.shutdown()

        #  print output to console
        json_parse_options = jsbeautifier.default_options()
        json_parse_options.indent_size = 4
        formatted_final_data = jsbeautifier.beautify(json.dumps(final_data), json_parse_options)
        print("output state: " + str(final_state) +
              "\noutput data: " + formatted_final_data)

        # write output to a json file which is stored in project folder
        with open("simulation_output.json", "w") as outfile:
            outfile.write(formatted_final_data)


def connect_simulator_to_agent_proxy(simulator_name):
    """
    create agent proxy and connect it to the right simulator name

    :param simulator_name:      (string) name of simulator
    :return:                    (agent)  agent object of the corresponding simulator
    """
    run_agent(simulator_name)
    agent_simulator = ns.proxy(simulator_name)
    agent_simulator.log_info(simulator_name + ' connected')
    return agent_simulator


if __name__ == '__main__':
    """
    Example executions of Orchestration algorithm. There are three test-cases:
    
    1. Using Gauss-Seidel coupling algorithm for two dual-dependent models
    2. Using Jacobi coupling algorithm for four CT or DE models which do not only depend on one model's output
    3. Using Jacobi coupling algorithm for three CT or DE open-source models
    """

    ns = run_nameserver()

    simulator_list_gauss = [{"name": "simulatorC", "factory": simulatorC_factory,
                             "dependency": ["simulatorE"], "order": 0},
                            {"name": "simulatorE", "factory": simulatorE_factory,
                             "dependency": ["simulatorC"], "order": 1}]

    simulator_list_jacobi = [{"name": "simulatorA", "factory": simulatorA_factory,
                              "dependency": ["simulatorB", "simulatorC"], "order": 1},
                             {"name": "simulatorB", "factory": simulatorB_factory,
                              "dependency": ["simulatorC", "simulatorA"], "order": 3},
                             {"name": "simulatorC", "factory": simulatorC_factory,
                              "dependency": ["simulatorB"], "order": 0},
                             {"name": "simulatorD", "factory": simulatorD_factory,
                              "dependency": ["simulatorB", "simulatorA"], "order": 2}]

    simulator_list_hybrid = [{"name": "simulatorHMM", "factory": simulatorHMM_factory,
                              "dependency": ["simulatorCiw"], "order": 0},
                             {"name": "simulatorCiw", "factory": simulatorCiw_factory,
                              "dependency": ["simulatorLG"], "order": 1},
                             {"name": "simulatorLG", "factory": simulatorLG_factory,
                              "dependency": ["simulatorHMM"], "order": 2}]

    initial_data_dict_gauss = {"simulatorC": [6], "simulatorE": [8, 19]}

    initial_data_dict_jacobi = {
        "simulatorA": 2, "simulatorB": [10, 15, 10, 11, 101], "simulatorC": 6, "simulatorD": [18, 21, 12]
    }

    initial_data_dict_hybrid = {
        "simulatorHMM": [
            [-0.17307679866920092, -1.0046970164746332],
            [11.163840145390036, -1.0574433375980758],
            [-0.5244943350032614, -0.07812436573441134],
            [0.3396166360722303, -0.10286418783911368],
            [0.562790707279984, 0.41179374282339065]
        ],
        "simulatorCiw": [0.20627254772273172],
        "simulatorLG": [0.08, 0.09]
    }

    jacobi_name_string = known_coupling_algorithms[1]
    gauss_name_string = known_coupling_algorithms[0]

    # simulation using Gauss-Seidel dual dependent coupling and Model C and E
    orchestrator_one = Orchestrator(gauss_name_string, simulator_list_gauss, initial_data_dict_gauss)

    # simulation using Jacobi coupling and Model A, B, C and D
    orchestrator_two = Orchestrator(jacobi_name_string, simulator_list_jacobi, initial_data_dict_jacobi)

    # simulation using Jacobi coupling and Model Ciw, HMM and LG
    orchestrator_three = Orchestrator(jacobi_name_string, simulator_list_hybrid, initial_data_dict_hybrid)

    # run the initialised orchestrator
    orchestrator_three.run_simulation()

    # ********** TEMPLATE TO ADD YOUR OWN MODELS TO THE SYSTEM **********
    # comment line 216 and un-commend line 222 to 232. Adjust the code to match your own simulation.
    #  Attention: Code below only works, when you've added your model to the template folder simulators_template

    # from simulators_template.Model_CT import CT_simulator_factory
    # from simulators_template.Model_DE import DE_simulator_factory
    #
    # simulator_list_demo = [{"name": "CTsimulator", "factory": CT_simulator_factory,
    #                         "dependency": ["DEsimulator"], "order": 0},
    #                        {"name": "DEsimulator", "factory": DE_simulator_factory,
    #                         "dependency": ["CTsimulator"], "order": 1}]
    # initial_data_dict_demo = {"CTsimulator": [7, 6], "DEsimulator": 8}
    #
    # orchestrator_demo = Orchestrator(jacobi_name_string, simulator_list_demo, initial_data_dict_demo)
    # orchestrator_demo.run_simulation()

    #  *******************************************************************
