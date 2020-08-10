import ciw


class ModelCiw:
    """
    code taken and modified from https://ciw.readthedocs.io/en/latest/Background/simulationpractice.html
    last visited: 10.08.2020
    """

    def __init__(self):
        self.number_of_servers = 1

    def run(self, event, state):
        """
        simulation of average waiting time of customers visiting a bank with a given amount of servers (event).

        :param event:       (int)  change in number of servers
        :param state:       (int)  current time step
        :return:            (list) list containing one entry: average waiting time
        """
        self.number_of_servers += event
        if self.number_of_servers <= 0:
            self.number_of_servers = 1

        N = ciw.create_network(
            arrival_distributions=[ciw.dists.Exponential(5.0)],
            service_distributions=[ciw.dists.Exponential(8.0)],
            routing=[[0.0]],
            number_of_servers=[self.number_of_servers]
        )
        average_waits = []
        warmup = 10
        cooldown = 10
        maxsimtime = 40

        for s in range(state + 1):
            ciw.seed(s)
            Q = ciw.Simulation(N)
            Q.simulate_until_max_time(warmup + maxsimtime + cooldown)
            recs = Q.get_all_records()
            waits = [r.waiting_time for r in recs if r.arrival_date > warmup and r.arrival_date < warmup + maxsimtime]
            try:
                average_waits.append(sum(waits) / len(waits))
            except ZeroDivisionError:
                pass
        try:
            average_wait = sum(average_waits) / len(average_waits)
        except ZeroDivisionError:
            average_wait = sum(average_waits)
        return average_wait

        # return_list = []
        # try:
        #     result = average_wait
        #     return_list.append(result)
        #     return return_list
        # except IndexError:
        #
        #     return_list.append(-1)
        #     return return_list


if __name__ == '__main__':
    model = ModelCiw()
    print(model.run(1, 3))
