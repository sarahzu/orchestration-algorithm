from pylab import *

# code taken from: https://math.libretexts.org/Bookshelves/Applied_Mathematics/Book%3A_Introduction_to_the_Modeling_and_Analysis_of_Complex_Systems_(Sayama)/06%3A_ContinuousTime_Models_I__Modeling/6.04%3A_Simulating_Continuous-Time_Models
# last visited: 08.08.2020

r = 0.2
K = 1.0
Dt = 1


class ModelCT:

    def initialize(self):
        global x, result, t, timesteps
        x = 0.1
        result = [x]
        t = 0.
        timesteps = [t]

    def observe(self):
        global x, result, t, timesteps
        result.append(x)
        timesteps.append(t)

    def update(self):
        global x, result, t, timesteps
        x = x + r * x * (1 - x / K) * Dt
        t = t + Dt

    def run(self):
        self.initialize()
        while t < 5:
            self.update()
            self.observe()
        print("timesteps: " + str(timesteps))
        print("timesteps: " + str(len(timesteps)))

        print("results: " + str(result))
        print("results: " + str(len(result)))



if __name__ == '__main__':
    model = ModelCT()
    model.run()



