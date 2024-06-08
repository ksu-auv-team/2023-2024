import cv2


cam = cv2.VideoCapture(0)

if not cam.isOpened():
    exit()
else:

    while True:
        ret, frame = cam.read()

        print(len(frame))
