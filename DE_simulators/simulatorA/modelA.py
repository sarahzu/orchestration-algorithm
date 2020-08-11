from termcolor import colored


class ModelA:
    """
    Example of a model class that is dependent on two other models and performs some easy mathematical computations
    to the input data.
    """

    def __init__(self):
        self.initial_data = [1, 2]

    def run(self, event, state):
        """
        run model execution

        :param event:       (int) event signal
        :param state:       (int) current state
        :return:            (int) model computed output data
        """
        try:
            return event + state
        except TypeError:
            print(colored("------------\n "
                          "the given event is not in the expected format:\nexpected: integer\nexpected: "
                          + str(type(event)) + "\n------------", 'yellow'))

