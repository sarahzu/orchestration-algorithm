from termcolor import colored


class ModelD:

    def __init__(self):
        self.initial_data = [18, 21]

    def run(self, data_list, state):
        try:
            current_data_entryB = data_list[0][state]
            current_data_entryA = data_list[1][state]
            self.initial_data.append(current_data_entryB - current_data_entryA * 5)
            return self.initial_data
        except TypeError:
            print(colored("------------\nwrong data type given to Model A\ninput type data: "
                          + str(type(data_list)) + "\nexpected input type data: list\ninput type time step: "
                          + str(type(state)) + "\nexpected input type time step: integer\n------------", 'yellow'))
            return None
        except IndexError:
            print(colored("------------\ngiven time step is not included in data array of Model A\ndata: "
                          + str(data_list) + "\ntime_step: " + str(state) + "\n------------", 'yellow'))
            return None

