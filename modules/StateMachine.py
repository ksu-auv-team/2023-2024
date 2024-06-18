from statemachine import StateMachine, State
from statemachine.contrib.diagram import DotGraphMachine

import json
import logging
import requests

# Import the necessary modules from the statemachine_modules folder

class AUVStateMachine(StateMachine):
    pass

if __name__ == '__main__':
    m = AUVStateMachine()
    graph = DotGraphMachine(m)
    dot = graph()
    dot.write_png('static/docs/state_machine.png')
