from termcolor import colored


class ModelB:
    """
    Example of a model class that is dependent on two other models and performs some easy mathematical computations
    to the input data.
    """

    def __init__(self):
        self.initial_data = [5, 6, 8, 9, 134]

    def get_data(self):
        return self.initial_data

    def run(self, data, state):
        """
        run model execution

        :param data:        (list) ct model input data list
        :param state:       (int)  current state
        :return:            (list) model computed output data list
        """
        try:
            current_data_entry_1 = data[0]
            current_data_entry_2 = data[1]
            self.initial_data[0] += current_data_entry_2 + 1 - current_data_entry_1 * 4
            self.initial_data[1] -= current_data_entry_2 + 1 - current_data_entry_1 * 4
            self.initial_data[2] -= current_data_entry_2 + 4 - current_data_entry_1 * 3
            self.initial_data[4] += current_data_entry_2 + 4 - current_data_entry_1 * 3
            return self.initial_data

        except IndexError:
            print(colored("------------\ngiven data has length " + str(len(data))
                          + " but should have length " + str(len(self.initial_data)) + "\n------------", 'yellow'))


