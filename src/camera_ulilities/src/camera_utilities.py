#!/usr/bin/python3

from numpysocket import NumpySocket
import cv2
import yaml

with open("configs/main.yml", "r") as f:
    configs = yaml.load(f, Loader=yaml.FullLoader)

cap = cv2.VideoCapture(configs["CAM"])

# Set camera frame rate
cap.set(cv2.CAP_PROP_FPS, configs["FPS"])

with NumpySocket() as s:
    s.connect((configs["Transmission_Location"], configs["Transmission_Port"]))
    while(cap.isOpened()):
        ret, frame = cap.read()
        frame_resize = cv2.resize(frame, (320, 180))
        if ret is True:
            try:
                s.sendall(frame_resize)
            except:
                break
        else:
            break
