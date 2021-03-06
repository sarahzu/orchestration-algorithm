from pylab import *
import random


class ModelLG:
    """
    CT logistic growth model
    """

    def __init__(self):
        self.initial_data = [9, 18]
        self.r = 0.2
        self.K = 1.0
        self.Dt = 1
        self.x = 0.1
        self.result = [self.x]

    def run(self, data_list, state):
        """
        run logistic growth model

        code partially taken from:
        https://math.libretexts.org/Bookshelves/Applied_Mathematics/Book%3A_Introduction_to_the_Modeling_and_Analysis_of_Complex_Systems_(Sayama)/06%3A_ContinuousTime_Models_I__Modeling/6.04%3A_Simulating_Continuous-Time_Models
        last visited: 08.08.2020
        """
        new_data_entry = self.x + self.r * self.x * (1 - self.x / self.K) * self.Dt * data_list[0][0][0] / random.randint(1, 10)
        self.initial_data[0] = new_data_entry
        self.initial_data[1] = new_data_entry * state
        return self.initial_data




