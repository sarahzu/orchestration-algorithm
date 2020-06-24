from osbrain import run_nameserver, run_agent
from simulatorA.simulatorA import SimulatorA
from simulatorB.simulatorB import SimulatorB
from simulator import Simulator
import time
import json


class Orchestrator:

    def __init__(self):
        self.simulatorA = SimulatorA("", "")
        self.simulatorB = SimulatorB("", "")

        self.time_step = ""
        self.data = ""

        # System deployment
        ns = run_nameserver()
        run_agent('SimulatorA')
        run_agent('SimulatorB')

        # Create a proxy to SimulatorA and log a message
        agent_simulatorA = ns.proxy('SimulatorA')
        agent_simulatorA.log_info('Hello world! Simulator A')

        # Create a proxy to SimulatorB and log a message
        agent_simulatorB = ns.proxy('SimulatorB')
        agent_simulatorB.log_info('Hello world! Simulator B')

        # System configuration
        addr_simulatorA = agent_simulatorA.bind('PUSH', alias='main')
        agent_simulatorB.connect(addr_simulatorA, handler=handler_simulatorB)

        # Send messages
        for _ in range(3):
            time.sleep(1)
            agent_simulatorA.send("main", "{\"timestep\": \"\", \"state\": \"\" }")

        ns.shutdown()


def handler_simulatorB(agent, message):
    try:
        input_json = json.loads(message)
        print(SimulatorB("", "").run_time_step(input_json["timestep"], input_json["state"]))
    except():
        print("wrong input")


if __name__ == '__main__':
    orchestrator = Orchestrator()
