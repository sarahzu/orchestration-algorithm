import ciw


class ModelCiw:

    def run(self, data_list, state):
        model_network = ciw.create_network(
            arrival_distributions=[ciw.dists.Exponential(0.2)],
            service_distributions=[ciw.dists.Exponential(0.1)],
            number_of_servers=[3]
        )
        ciw.seed(1)
        simulation = ciw.Simulation(model_network)
        if state == 0:
            state += 1
        simulation.simulate_until_max_time(1440 + state)

        return_list = []
        try:
            ind = simulation.nodes[-1].all_individuals[0]
            # data[0].append(int(ind.data_records[0].arrival_date))
            #  return data[0]
            result = int(ind.data_records[0].arrival_date)
            result += state + data_list[0][0]
            return_list.append(result)
            return return_list
        except IndexError:
            # data.append(-1)
            # return data[0]
            return_list.append(-1)
            return return_list

