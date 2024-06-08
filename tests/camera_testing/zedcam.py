import cv2


cam = cv2.VideoCapture(0)
if cam.isOpened():
    continue
else:
    print('failed')

while True:
    ret, frame = cam.read()

    print(len(frame))
