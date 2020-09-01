# Orchestration Algorithm
This project implements a co-simulation orchestration algorithms capable of hybrid co-simulation including two different coupling algorithms: Gauss-Seidel and Jacobi coupling algorithm. It uses an agent based system which handles the simulator and model executions. Wrapper classes are responsible to perform the model exchange between Continuous Time (CT) and Discrete Event (DE) models. It is designed in an abstract way but it's adaptable structure allows it to be used for specific use-cases as well.

The file _orchestrator.py_ is the main file of the project. It includes the _Orchestrator_ class responsible for running the simulation. The _Orchestrator_ class needs the following parameter values:
1. (String) The name of the used coupling algorithm: either _"gauss-seidel"_ or _"jacobi"_
2. (List) A list containing the needed information about the used simulators: name, which factory class is used to create the simulator, on which other simulator's output it depends on and the order of execution. The list is structured in the form: 

    [{"name": "simulatorA", "factory": simulatorA_factory, "dependency": ["simulatorB"], "order": 0}, 
    
    {"name": "simulatorB", "factory": simulatorB_factory, "dependency": ["simulatorA"], "order": 1}]
3. (Dictionary) The initial data for every simulator in the form: 

    {"simulatorA": [9, 2], "simulatorB": 2.0234203}

The _orchestrator.py_ file contains a main function which runs one use case of the simulation. The function defines an Orchestration objects and calls its run function. The code structure is as follows:
```
orchestrator = Orchestrator(coupling_algorithm_name, simulator_list, initial_data_dict)
orchestrator.run_simulation()
```
By changing the values of _coupling_algorithm_name_, _simulator_list_ and _initial_data_dict_, the simulation can be changed. Before the first run, all required libraries have to be downloaded by executing the following command: 
```
pip install -r requirements.txt.
```

The simulation can then be run by executing the following command: 
```
python orchestrator.py 
```
Per default, the _Orchestrator_ simulates three models:
* A DE model simulating the waiting time of customers visiting a bank (open-source model called _CIW_ [1])
* A CT Hiden Markov Model (using the open-source library _hmmlearn_ [2])
* A CT logistic growth model [3]

The simulation results are written in a JSON file called _simulation_output.json_ which is located in the root folder and contains every result for every computed time step and model. The results are also printed on the terminal.

## References
[1] Palmer, Geraint I., et al. "Ciw: An open-source discrete event simulation library." _Journal of Simulation_ 13.1 (2019): 68-82. [Website](https://ciw.readthedocs.io/en/latest/index.html)

[2] hmmlearn developers (2010). hmmlearn. [Website](https://hmmlearn.readthedocs.io/en/latest/)

[3] Hiroki Sayama (2020). Simulating Continuous-Time Models. _OpenSUNY_. [Website](https://math.libretexts.org/Bookshelves/Applied_Mathematics/Book%3A_Introduction_to_the_Modeling_and_Analysis_of_Complex_Systems_(Sayama)/06%3A_ContinuousTime_Models_I__Modeling/6.04%3A_Simulating_Continuous-Time_Models)
