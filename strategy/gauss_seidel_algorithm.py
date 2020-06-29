from strategy.strategy_algorithm import StrategyAlgorithm


class GaussSeidelAlgorithm(StrategyAlgorithm):

    def __init__(self):
        super().__init__()

    def algorithm(self, min_time_step, time_step, max_time_step, execution_method,
                  agent_simulatorA, agent_simulatorB, initial_input):
        simulatorA_output = initial_input

        while min_time_step <= time_step < max_time_step:
            # execute simulator B with output from simulator A
            simulatorB_output = execution_method(agent_simulatorB, simulatorA_output, 'mainA')
            print("SimulatorB output: " + str(simulatorB_output))

            # execute simulator A with output from simulator B
            simulatorA_output = execution_method(agent_simulatorA, simulatorB_output, 'mainB')
            time_step += 1
            print("SimulatorA output: " + str(simulatorA_output))
