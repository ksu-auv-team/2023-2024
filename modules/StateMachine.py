import json
import logging
import requests
import numpy as np


# Import the necessary modules from the statemachine_modules folder

class AUVStateMachine:
    def __init__(self):
        self.movements = {
            "forward": [1, 0, 0, 0, 0, 0, 0, 0, 0],
            "backward": [-1, 0, 0, 0, 0, 0, 0, 0, 0],
            "left": [0, 1, 0, 0, 0, 0, 0, 0, 0],
            "right": [0, -1, 0, 0, 0, 0, 0, 0, 0],
            "up": [0, 0, 1, 0, 0, 0, 0, 0, 0],
            "down": [0, 0, -1, 0, 0, 0, 0, 0, 0],
            "yaw_left": [0, 0, 0, 1, 0, 0, 0, 0, 0],
            "yaw_right": [0, 0, 0, -1, 0, 0, 0, 0, 0],
        }