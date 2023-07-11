import cv2
import numpy as np

from src.modules.networking.networking import Networking

# ... image_resize function ...

class Regular:
    def __init__(self, host, port, camera_id):
        self.host = host
        self.port = port
        try:
            self.cam = cv2.VideoCapture(camera_id)
        except Exception as e:
            print("Error initializing camera: ", e)
        self.connect()

    def connect(self):
        try:
            self.np_socket = Networking()
            self.np_socket.bind((self.host, self.port))
            self.np_socket.listen(1)
            self.client, _ = self.np_socket.accept()
            print('Client connected')
        except Exception as e:
            print("Error in connect: ", e)

    def send_frame(self):
        try:
            ret, frame = self.cam.read()
            if not ret:
                print("Failed to get frame")
                return
            frame = image_resize(frame, width=480) # Resize to lower the data
            frame = np.array(frame, dtype='uint8') # Ensure the datatype
            self.client.send_numpy(frame)
        except Exception as e:
            print("Error in send_frame: ", e)

    def close(self):
        try:
            self.client.close()
            self.np_socket.close()
            self.cam.release()
        except Exception as e:
            print("Error in close: ", e)

    def run(self):
        try:
            while True:
                self.send_frame()
        except KeyboardInterrupt:
            print("Interrupted")
        finally:
            self.close()

if __name__ == '__main__':
    try:
        camera = Regular('localhost', 9999, 0)
        camera.run()
    except Exception as e:
        print("Error in main: ", e)
