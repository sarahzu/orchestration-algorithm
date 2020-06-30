from strategy.strategy_algorithm import StrategyAlgorithm


class GaussSeidelAlgorithm(StrategyAlgorithm):

    def __init__(self):
        super().__init__()

    def algorithm(self, min_time_step, time_step, max_time_step, agent_simulatorA, name_agent_simulatorA,
                  agent_simulatorB, name_agent_simulatorB, initial_input, communication_step):

        simulatorA_output = initial_input
        while min_time_step <= time_step < max_time_step:
            # execute simulator B with output from simulator A
            simulatorB_output = self.execute_simulator_with_output_from_other_simulator(
                agent_simulatorB, simulatorA_output, name_agent_simulatorA, time_step)
            print("SimulatorB output: " + str(simulatorB_output))

            # execute simulator A with output from simulator B
            simulatorA_output = self.execute_simulator_with_output_from_other_simulator(
                agent_simulatorA, simulatorB_output, name_agent_simulatorB, time_step)
            print("SimulatorA output: " + str(simulatorA_output))

            # increase time_step by the given communication step
            time_step += communication_step

        return time_step, simulatorA_output
