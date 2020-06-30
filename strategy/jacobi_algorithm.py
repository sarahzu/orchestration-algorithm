from strategy.strategy_algorithm import StrategyAlgorithm


class JacobiAlgorithm(StrategyAlgorithm):

    def __init__(self):
        super().__init__()

    def algorithm(self, min_state, state, max_state, agent_simulator_object_list, agent_simulator_name_list,
                  initial_input, time_step):
        #  TODO: implement jacobi algorithm
        return state, initial_input
