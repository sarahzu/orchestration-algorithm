from termcolor import colored


class ModelE:
    """
    Example of a model class that is dependent on one other model and performs some easy mathematical computations
    to the input data.
    """

    def __init__(self):
        self.initial_data = [8, 19]

    def run(self, data_list, state):
        """
        run model execution

        :param data_list:   (list) model input data list
        :param state:       (int)  current state
        :return:            (list) model computed output data list
        """
        try:
            current_data_entry = data_list[0][state]
            self.initial_data.append(current_data_entry * 17)
            return self.initial_data
        except TypeError:
            print(colored("------------\nwrong data type given to Model A\ninput type data: "
                          + str(type(data_list[0])) + "\nexpected input type data: list\ninput type time step: "
                          + str(type(state)) + "\nexpected input type time step: integer\n------------", 'yellow'))
            return None
        except IndexError:
            print(colored("------------\ngiven time step is not included in data array of Model A\ndata: "
                          + str(data_list[0]) + "\ntime_step: " + str(state) + "\n------------", 'yellow'))
            return None

