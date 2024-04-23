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
from socket import AF_INET, SOCK_STREAM

# Importing the custom networking protocol
from modules.NetworkingProtocol import NetworkingProtocol

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

# Setting up the networking protocol
def setup_networking_protocol(host: str = 'localhost', port: int = 5000):
    # Creating the server socket
    server_socket = NetworkingProtocol(AF_INET, SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    # Accepting the connection
    logging.info("Waiting for connection...")
    client_socket, addr = server_socket.accept()
    logging.info(f"Connection established with {addr}")

    return server_socket, client_socket

# Main function
def main(args: list = sys.argv):
    pass


# Running the main function
if __name__ == "__main__":
    main()