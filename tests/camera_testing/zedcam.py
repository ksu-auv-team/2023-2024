import cv2


cam = cv2.VideoCapture(1)
if cam.isOpened():
    continue
else:
    print('failed')
