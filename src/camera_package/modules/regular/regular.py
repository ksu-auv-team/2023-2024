import cv2
from src.modules.networking import Networking

class Regular:
    def __init__(self, host, port, camera_id):
        self.host = host
        self.port = port
        self.camera_id = camera_id
        self.cam = cv2.VideoCapture(self.camera_id)
        self.np_socket = Networking()

    def start(self):
        # Start the server
        self.np_socket.start_server(self.host, self.port)
        print(f"Server started at {self.host}:{self.port}")
        
        print("Waiting for a connection...")
        self.client_socket = self.np_socket.accept_connection()
        print("Client connected")

        while True:
            # Capture a frame
            ret, frame = self.cam.read()

            if not ret:
                print("Failed to capture frame")
                break

            # Send the frame
            self.client_socket.send_numpy(frame)

        # Release the webcam and close the socket when done
        self.cam.release()
        self.np_socket.close_connection()

if __name__ == "__main__":
    HOST = 'localhost'  # or your IP
    PORT = 9999  # or your port
    CAMERA_ID = 0  # or your camera id

    server = Regular(HOST, PORT, CAMERA_ID)
    server.start()
