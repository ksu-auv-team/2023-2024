import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import cv2
from src.modules.networking.networking import Networking


so = Networking()
so.connect('10.0.0.34', 9999)

while True:
    image = so.recv_numpy()
    cv2.imshow('image', image)
    if cv2.WaitKey(1) & 0xFF == ord('q'):
        break