import socket  # Import socket module for networking
import logging  # Import logging module for debugging and tracking
import numpy as np  # Import numpy module for mathematical operations and handling arrays
from io import BytesIO  # Import BytesIO for handling binary streams

# Define a class Networking that extends the socket class
class Networking(socket.socket):
    # Initialize the class
    def __init__(self, *args, **kwargs):
        # Call to parent's constructor
        super().__init__(*args, **kwargs)
        # Set the default buffer size
        self.buffer_size = 1024

    # Connect to a server at host and port
    def connect_server(self, host, port):
        super().connect((host, port))
        logging.debug(f"Connected to {host}:{port}")  # Log connection

    def start_server(self, host, port):
        super().bind((host, port))
        super().listen(1)
        logging.debug(f"Server started at {host}:{port}")  # Log server start

    # New function to accept a connection
    def accept_connection(self):
        client_socket, addr = super().accept()
        client_socket = self.__class__(fileno=client_socket.fileno())
        logging.debug(f"Accepted connection from {addr}")  # Log connection
        return client_socket

    # Send a numpy array to the connected server
    def send_numpy(self, array):
        if not isinstance(array, np.ndarray):  # Check if the input is a numpy array
            raise TypeError("Input should be a numpy array")
        data = self._pack_numpy(array)  # Pack the numpy array
        print(f"Sending array of length {len(data)}")
        print(f"Original array shape: {array.shape}, dtype: {array.dtype}")
        self.sendall(data)  # Send all the data
        logging.debug("Array sent")  # Log the send

    # Receive a numpy array from the connected server
    def recv_numpy(self):
        data = self._recvall()  # Receive all the data
        print(f"Received data of length {len(data)}")
        # Load the numpy array from the data received
        array = np.load(BytesIO(data), allow_pickle=True)['array']
        logging.debug("Array received")  # Log the receive
        return array  # Return the array

    # Receive all the data until 'END\n' is found
    def _recvall(self):
        data = bytearray()  # Initialize a bytearray to store data
        while len(data) < 4 or data[-4:] != b'END\n':  # While loop to receive data until 'END\n' is found
            packet = self.recv(self.buffer_size)  # Receive data in packets of buffer_size
            if not packet:  # If no packet is received, break the loop
                break
            data.extend(packet)  # Add the packet data to the total data
        return data[:-4]  # Return all the data except the last 4 bytes 'END\n'

    # Pack the numpy array into binary format
    @staticmethod
    def _pack_numpy(array):
        f = BytesIO()  # Initialize a BytesIO stream
        np.savez(f, array=array)  # Save the numpy array into the stream
        data = f.getvalue() + b'END\n'  # Get the binary data from the stream and append 'END\n' 
        return data  # Return the data

    # Close the socket connection
    def close_connection(self):
        self.close()  # Close the socket
        logging.debug("Connection closed")  # Log closure
