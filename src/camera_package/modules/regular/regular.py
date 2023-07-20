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
        self.np_socket.bind(self.host, self.port)
        self.np_socket.listen(1)
        print(f"Server started at {self.host}:{self.port}")

        print("Waiting for a connection...")
        self.client_socket, _ = self.np_socket.accept()
        print("Client connected")

        while True:
            # Capture a frame
            ret, frame = self.cam.read()

            if not ret:
                print("Failed to capture frame")
                break

            # # Send the frame
            self.client_socket.send_numpy(frame)  # Use self.np_socket to send the frame

        # Release the webcam and close the socket when done
        self.cam.release()
        self.np_socket.close()

if __name__ == "__main__":
    HOST = '10.0.0.34'  # or your IP
    PORT = 9999  # or your port
    CAMERA_ID = 0  # or your camera id

    server = Regular(HOST, PORT, CAMERA_ID)
    server.start()
