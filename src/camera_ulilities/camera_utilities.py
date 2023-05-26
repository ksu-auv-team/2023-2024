#!/usr/bin/python3

from numpysocket import NumpySocket
import cv2
import yaml

from typing import int, dict, str, Optional

class CameraUtilities:
    def __init__(self, cam: int, fps:int = 30, dest: str = 'localhost', port: int = 9996):
        self.cap = cv2.VideoCapture(cam)

        # Set camera frame rate
        self.cap.set(cv2.CAP_PROP_FPS, fps)

        self.dest = dest        
        self.port = port

    def run(self):
        with NumpySocket() as s:
            s.connect((self.dest, self.port))
            while(self.cap.isOpened()):
                ret, frame = self.cap.read()
                frame_resize = cv2.resize(frame, (320, 180))
                if ret is True:
                    try:
                        s.sendall(frame_resize)
                    except:
                        break
                else:
                    break
