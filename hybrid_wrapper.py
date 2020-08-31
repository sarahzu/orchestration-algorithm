

class HybridWrapper:
    """
    Abstract Wrapper class used for hybrid co-simulation
    """

    def run(self, data, state):
        """
        abstract run function which runs a model with transformed input data

        :param data:   (list) input data
        :param state:  (int)  current state
        :return:
        """
        pass
