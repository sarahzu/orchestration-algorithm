

class Simulator:
    """
    Abstract simulator class
    """

    def __init__(self):
        pass

    def run_state(self, state, data):
        """
        abstract definition of function that runs model of the simulator

        :param state:   (int)  current state
        :param data:    (list) data input list for model execution
        :return:        (dict) model output data dict
        """
        pass
