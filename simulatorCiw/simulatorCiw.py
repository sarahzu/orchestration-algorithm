import ciw
from osbrain import Agent

from simulator import Simulator
from simulatorCiw.modelCiw import ModelCiw


class SimulatorCiw(Simulator, Agent):

    def __init__(self):
        super().__init__()
        self.model = ModelCiw()

    def run_state(self, state, data):
        """
        run function for a CIW model

        :param state: (int)  current state of the simulation
        :param data:  (list) previously computed data
        """
        model_network = self.model.run()
        simulation = ciw.Simulation(model_network)
        if state == 0:
            state += 1
        simulation.simulate_until_max_time(1440 + state)

        return_list = []
        try:
            ind = simulation.nodes[-1].all_individuals[0]
            # data[0].append(int(ind.data_records[0].arrival_date))
            # return data[0]
            return_list.append(int(ind.data_records[0].arrival_date))
            return return_list
        except IndexError:
            # data.append(-1)
            # return data[0]
            return_list.append(-1)
            return return_list
