import cv2
from src.modules.networking import Networking

class WebcamClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.np_socket = Networking()

    def start(self):
        # Connect to the server
        self.np_socket.connect_server(self.host, self.port)
        print(f"Connected to the server at {self.host}:{self.port}")

        while True:
            # Receive a frame
            frame = self.np_socket.recv_numpy()

            # Display the frame
            cv2.imshow("Webcam", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Close the window when done
        cv2.destroyAllWindows()
        self.np_socket.close_connection()

if __name__ == "__main__":
    HOST = '10.0.0.34'  # or the server IP
    PORT = 9999  # or the server port

    client = WebcamClient(HOST, PORT)
    client.start()
