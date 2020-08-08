import ciw


class ModelCiw:

    def run(self):
        model_network = ciw.create_network(
            arrival_distributions=[ciw.dists.Exponential(0.2)],
            service_distributions=[ciw.dists.Exponential(0.1)],
            number_of_servers=[3]
        )
        ciw.seed(1)
        return model_network

