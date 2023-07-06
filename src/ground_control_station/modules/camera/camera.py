import numpy as np
from numpysocket import NumpySocket
import cv2


class Camera:
    def __init__(self, host, port, camera_id):
        self.id = camera_id
        self.host = host
        self.port = port
        self.np_socket = NumpySocket()
        self.np_socket.connect((self.host, self.port))

    def get_frame(self) -> tuple:
        frame = self.np_socket.recv()
        if frame == 0:
            return None, None
        data = frame[0]
        img = frame[1]
        return data, img
    
    def run(self):
        while True:
            data, img = self.get_frame()
            if data == 0:
                break
            cv2.imshow('frame', img)
            print(data)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        self.np_socket.close()
        print('Camera {} closed'.format(self.id))
        
    
if __name__ == '__main__':
    camera = Camera('localhost', 9999, 0)
    camera.run()