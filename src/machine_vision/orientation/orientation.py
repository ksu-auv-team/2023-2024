# Import necessary python libraries
import os
import sys
import cv2
import yaml
import time
import numpy as np
from numpysocket import NumpySocket
from datetime import datetime


# get the current working directory
HOME = os.getcwd()
print(HOME)

# load the configuration file
config_path = HOME + '/src/machine_vision/configs/orientation.yaml'
with open(config_path, 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# define the ip and port for the numpy socket (within the config file)
ip = config['ip']
port = config['port']

# Create the class for the orientation detection
class orientation:
    def __init__(self):
        pass
    
    def socket(self):
        pass
    
    def detect(self):
        pass