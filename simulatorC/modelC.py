from termcolor import colored


class ModelC:
    """
    Example of a model class that is dependent on one other model and performs some easy mathematical computations
    to the input data.
    """

    def __init__(self):
        self.initial_data = [9, 18]

    def run(self, data_list, state):
        """
        run model execution

        :param data_list:   (list) model input data list
        :param state:       (int)  current state
        :return:            (list) model computed output data list
        """
        try:
            try:
                current_data_entry = data_list[0][state]
            except (IndexError, TypeError) as e:
                current_data_entry = data_list[0][0]
            self.initial_data.append(current_data_entry + 100)
            return self.initial_data
        except TypeError:
            print(colored("------------\nwrong data type given to Model C\ninput type data: "
                          + str(type(data_list[0])) + "\nexpected input type data: list\ninput type time step: "
                          + str(type(state)) + "\nexpected input type time step: integer\n------------", 'yellow'))
            return []
        except IndexError:
            print(colored("------------\ngiven time step is not included in data array of Model C\ndata: "
                          + str(data_list[0]) + "\ntime_step: " + str(state) + "\n------------", 'yellow'))
            return []

