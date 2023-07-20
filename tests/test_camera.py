import cv2
import numpy as np
from src.modules.networking.networking import Networking

class Client:
    """
    The Client class encapsulates the functionality of receiving frames from a server and displaying them.

    Attributes:
        host (str): The host address where the socket server runs.
        port (int): The port number where the socket server listens.
        np_socket: A Networking socket instance to receive data from the server.
    """
    def __init__(self, host, port):
        """
        Initialize an instance of the Client class.

        Args:
            host (str): The host address where the socket server runs.
            port (int): The port number where the socket server listens.
        """
        self.host = host
        self.port = port
        self.connect()

    def connect(self):
        """
        Connect to the server.

        Raises:
            Exception: An error occurred creating the socket connection.
        """
        try:
            # Create a networking socket
            self.np_socket = Networking()
            # Connect the socket to the host and port
            self.np_socket.connect(self.host, self.port)
            print("Connected to the server")
        except Exception as e:
            print("Error in connect: ", e)

    def receive_frame(self):
        """
        Receive a frame from the server and display it.

        Raises:
            Exception: An error occurred receiving data or displaying the frame.
        """
        try:
            # Receive a frame from the server as a numpy array
            frame = self.np_socket.recv_numpy()
            # Display the frame
            cv2.imshow("Video", frame)
            cv2.waitKey(1)
        except Exception as e:
            print("Error in receive_frame: ", e)

    def close(self):
        """
        Close the socket connection.

        Raises:
            Exception: An error occurred closing the connection.
        """
        try:
            # Close the socket
            self.np_socket.close()
        except Exception as e:
            print("Error in close: ", e)

    def run(self):
        """
        Enter a loop to continuously receive frames from the server and display them, 
        until a keyboard interrupt is detected. Then, gracefully close the resources.
        """
        try:
            # Continuously receive frames from the server and display them
            while True:
                self.receive_frame()
        except KeyboardInterrupt:
            print("Interrupted")
        finally:
            # Gracefully close the resources when done
            self.close()

# Run the client as a standalone application for debugging purposes
if __name__ == '__main__':
    try:
        # Create the Client object and start receiving frames
        client = Client('10.0.0.34', 9999)
        client.run()
    except Exception as e:
        print("Error in main: ", e)
