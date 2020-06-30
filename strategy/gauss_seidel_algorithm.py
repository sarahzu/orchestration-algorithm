from strategy.strategy_algorithm import StrategyAlgorithm


class GaussSeidelAlgorithm(StrategyAlgorithm):

    def __init__(self):
        super().__init__()

    def algorithm(self, min_state, state, max_state, agent_simulator_object_list, agent_simulator_name_list,
                  initial_input, time_step):

        next_simulator_input = initial_input
        while min_state <= state < max_state:
            for agent_simulator, agent_simulator_name in zip(agent_simulator_object_list, agent_simulator_name_list):
                # execute simulator B with output from simulator A
                simulator_output = self.execute_simulator_with_output_from_other_simulator(
                    agent_simulator, next_simulator_input, agent_simulator_name, state)
                print(str(agent_simulator_name) + " output: " + str(simulator_output))
                next_simulator_input = simulator_output

            # increase state by the given time step
            state += time_step

        return state, next_simulator_input
