from termcolor import colored


class ModelD:
    """
    Example of a model class that is dependent on two other models and performs some easy mathematical computations
    to the input data.
    """

    def __init__(self):
        self.initial_data = [18, 21, 83]

    def get_data(self):
        return self.initial_data

    def run(self, data_list, state):
        """
        run model execution

        :param data_list:   (list) model input data list
        :param state:       (int)  current state
        :return:            (list) model computed output data list
        """
        try:
            current_data_entry_1 = data_list[0]
            current_data_entry_2 = data_list[1]
            self.initial_data[0] += current_data_entry_1 - current_data_entry_2 * 5
            self.initial_data[1] -= current_data_entry_1 - current_data_entry_2 * 5
            self.initial_data[2] += current_data_entry_1 - current_data_entry_2 * 9
            return self.initial_data
        except IndexError:
            print(colored("------------\ngiven data has length " + str(len(data_list[0])) + " and "
                          + str(len(data_list[1]))
                          + " but should have length " + str(len(self.initial_data)) + "\n------------", 'yellow'))

