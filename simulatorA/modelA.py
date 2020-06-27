from termcolor import colored


class ModelA:

    def __init__(self):
        pass

    def run(self, data, time_step):
        try:
            data[time_step] = data[time_step] + 11
            return data
        except TypeError:
            print(colored("------------\nwrong data type given to Model A\ninput type data: "
                          + str(type(data)) + "\nexpected input type data: list\ninput type time step: "
                          + str(type(time_step)) + "\nexpected input type time step: integer\n------------", 'yellow'))
            return None
        except IndexError:
            print(colored("------------\ngiven time step is not included in data array of Model A\ndata: "
                          + str(data) + "\ntime_step: " + str(time_step) + "\n------------", 'yellow'))
            return None

