from termcolor import colored


class ModelB:

    def __init__(self):
        pass

    def run(self, data_list, state):
        try:
            current_data_entryC = data_list[0][state]
            current_data_entryA = data_list[1][state]
            data_list[0][state] = current_data_entryA + 1 - current_data_entryC * 4
            return data_list[0]
        except TypeError:
            print(colored("------------\nwrong data type given to Model B\ninput type data: "
                          + str(type(data_list[0])) + "\nexpected input type data: list\ninput type time step: "
                          + str(type(state)) + "\nexpected input type time step: integer\n------------", 'yellow'))
            return None
        except IndexError:
            print(colored("------------\ngiven time step is not included in data array of Model B\ndata: "
                          + str(data_list[0]) + "\ntime_step: " + str(state) + "\n------------", 'yellow'))
            return None


