import cv2
import numpy as np
from src.modules.networking import Networking

class WebcamClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = Networking()

    def start(self):
        # Connect to the server
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to the server at {self.host}:{self.port}")

        while True:
            # Receive a frame
            frame = self.client_socket.recv_numpy()

            # Display the frame
            cv2.imshow("Webcam", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Close the window and the socket when done
        cv2.destroyAllWindows()
        self.client_socket.close()

if __name__ == "__main__":
    HOST = '10.0.0.34'  # or the server IP
    PORT = 9999  # or the server port

    client = WebcamClient(HOST, PORT)
    client.start()
