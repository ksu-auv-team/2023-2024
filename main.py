"""
    Main file for the project.
    For now this script handles the backend subprocesses of the project.
    Four sub-processes are handles:
        - Hardware Interface
        - Movement Package
        - Neural Network Package
        - Web Interface

    These four sub-processes will be run in parallel to each other and communicate via the custom networking protocol.

    The main script will be responsible for handling the communication between the sub-processes and the handling of the state machine.
    The state machine will be responsible for the overall control of the project.
"""

# Importing the necessary libraries
import subprocess
import argparse
import sys
import os
import time

# Import the necessary modules
from modules.HardwareInterface import HardwareInterface
from modules.MovementPackage import MovementPackage
from modules.NeuralNetwork import NeuralNetworkPackage
from modules.WebInterface import WebInterface
from modules.StateMachine import StateMachine

# Creating the custom logger
import logging
logging.basicConfig(
    filename='logs/main.log',      # Name of the log file
    filemode='a',            # Append mode (use 'w' for overwrite each time)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    datefmt='%Y-%m-%d %H:%M:%S',  # Timestamp format
    level=logging.INFO       # Minimum log level to record
)

# Main function
def main(args: list = sys.argv):
    pass


# Running the main function
if __name__ == "__main__":
    main()