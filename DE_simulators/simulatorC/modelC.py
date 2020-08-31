import math

from termcolor import colored


class ModelC:
    """
    Example of a model class that is dependent on one other model and performs some easy mathematical computations
    to the input data.
    """

    def run(self, event, state):
        """
        run model execution

        :param event:       (string) model input event signal
        :param state:       (int)    current state
        :return:            (int)    model computed output data
        """
        try:
            return event + 2 * state
        except TypeError:
            print(colored("------------\n "
                          "the given event is not in the expected format:\nexpected: integer\nexpected: "
                          + str(type(event)) + "\n------------", 'yellow'))

