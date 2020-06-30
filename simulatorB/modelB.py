from termcolor import colored


class ModelB:

    def __init__(self):
        pass

    def run(self, data, time_step):
        try:
            current_data_entry = data[time_step]
            data[time_step] = current_data_entry + 1
            return data
        except TypeError:
            print(colored("------------\nwrong data type given to Model B\ninput type data: "
                          + str(type(data)) + "\nexpected input type data: list\ninput type time step: "
                          + str(type(time_step)) + "\nexpected input type time step: integer\n------------", 'yellow'))
            return None
        except IndexError:
            print(colored("------------\ngiven time step is not included in data array of Model B\ndata: "
                          + str(data) + "\ntime_step: " + str(time_step) + "\n------------", 'yellow'))
            return None


