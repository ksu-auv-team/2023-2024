
from src.modules.networking.networking import Networking
import cv2

class Camera:
    def __init__(self, host, port, camera_id):
        self.host = host
        self.port = port
        self.camera_id = camera_id

        self.np_socket = Networking()
        self.np_socket.connect(self.host, self.port)

    def connect(self):
        pass

    def get_frame(self):
        pass
    
    def close(self):
        pass

    def run(self):
        pass

if __name__ == '__main__':
    pass