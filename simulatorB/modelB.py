from termcolor import colored


class ModelB:
    """
    Example of a model class that is dependent on two other models and performs some easy mathematical computations
    to the input data.
    """

    def __init__(self):
        self.initial_data = [5, 6]

    def run(self, data_list, state):
        """
        run model execution

        :param data_list:   (list) model input data list
        :param state:       (int)  current state
        :return:            (list) model computed output data list
        """
        try:
            current_data_entryC = data_list[0][state]
            current_data_entryA = data_list[1][state]
            self.initial_data.append(current_data_entryA + 1 - current_data_entryC * 4)
            return self.initial_data
        except TypeError:
            print(colored("------------\nwrong data type given to Model B\ninput type data: "
                          + str(type(data_list[0])) + "\nexpected input type data: list\ninput type time step: "
                          + str(type(state)) + "\nexpected input type time step: integer\n------------", 'yellow'))
            return None
        except IndexError:
            print(colored("------------\ngiven time step is not included in data array of Model B\ndata: "
                          + str(data_list[0]) + "\ntime_step: " + str(state) + "\n------------", 'yellow'))
            return None


