from json.decoder import JSONDecodeError
from osbrain import run_nameserver, run_agent
from simulatorA.simulatorA import SimulatorA
from simulatorB.simulatorB import SimulatorB
import json
import random
from termcolor import colored
from strategy.gauss_seidel_algorithm import GaussSeidelAlgorithm
from strategy.jacobi_algorithm import JacobiAlgorithm

initial_data = random.sample(range(10), 10)
max_state = 9
min_state = 0
curr_state = 0
communication_step = 1

simulatorA = SimulatorA(curr_state, initial_data)
simulatorB = SimulatorB(curr_state, initial_data)

# System deployment
ns = run_nameserver()
envA = run_agent('SimulatorA', attributes=dict(data=initial_data))
envB = run_agent('SimulatorB', attributes=dict(data=initial_data))

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

    def run_simulation(self):
        """
        connect all simulators to an agent and let them run

        :return:
        """
        # Create a proxy to SimulatorA and log a message
        agent_simulatorA = ns.proxy('SimulatorA')
        agent_simulatorA.log_info('Simulator A connected')

        # Create a proxy to SimulatorB and log a message
        agent_simulatorB = ns.proxy('SimulatorB')
        agent_simulatorB.log_info('Simulator B connected')

        # System configuration:
        # connect agent of simulator A with agent of simulator B and vis versa
        addr_simulatorA = agent_simulatorA.bind('REP', alias='mainA', handler=handler_simulatorB)
        agent_simulatorB.connect(addr_simulatorA, alias='mainA')
        addr_simulatorB = agent_simulatorB.bind('REP', alias='mainB', handler=handler_simulatorA)
        agent_simulatorA.connect(addr_simulatorB, alias='mainB')

        # initial simulatorA output
        simulatorA_output = {
            "state": self.state,
            "data": self.data
        }

        # depending on used algorithm, execute different strategy
        if self.algorithm.lower() == 'gauss-seidel':
            # run gauss seidel algorithm
            gauss_seidel_algorithm = GaussSeidelAlgorithm()
            final_state, final_data = gauss_seidel_algorithm.algorithm(
                min_state, self.state, max_state, agent_simulatorA, 'mainA',
                agent_simulatorB, 'mainB', simulatorA_output, self.time_step)

            print("final state: " + str(final_state) + "\nfinal data: " + str(final_data['data']))

        elif self.algorithm.lower() == 'jacobi':
            # run jacobi algorithm
            jacobi_algorithm = JacobiAlgorithm()
            final_state, final_data = jacobi_algorithm.algorithm(
                min_state, self.state, max_state, agent_simulatorA, 'mainA',
                agent_simulatorB, 'mainB', simulatorA_output, self.time_step)

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
    orchestrator = Orchestrator('Gauss-Seidel')
    orchestrator.run_simulation()
