from ultralytics import YOLO
import cv2
import numpy as np
from services.WebCamService import WebCam

#commented out as this is work in progress and leaving as is causes errors
def frames(cNum):  
    while True:
        if cNum == 0:
            success, frame = camera_0.read()
            print("Zed camera:")
        else:
            #will have 2nd ip after testing 2nd camera
            #success, frame = camera_1.read()
            print("2nd Webcam:")
            break
        if not success:
            break
        else:
            center_x , center_y = box_center(frame)
            # 240x320 is half the dimension of the cameras tested
            # adjust these values depending on your cameras resolution
            adjust_camera(center_x, center_y, 240, 320)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# find the center of the objects bounding box when detected
def box_center(frame):
    results = model.predict(frame)
    for result in results:
        for box in result.boxes:
            left, top, right, bottom = np.array(box.xyxy.cpu(), dtype=np.int).squeeze()
            center_x = (left + right) // 2
            center_y = (top + bottom) // 2
    return center_x, center_y



def adjust_camera(center_x, center_y, frame_center_x, frame_center_y):
    centered_x = False
    centered_y = False

    # tolerance used to represent room for error
    # decrease to make function less lenient, increase to make more lenient
    tolerance = 40
    if center_x < frame_center_x - tolerance:
        print("Move camera to the left")
    elif center_x > frame_center_x + tolerance:
        print("Move camera to the right")
    else:
        centered_x = True
    
    if center_y < frame_center_y - tolerance:
        print("Move camera up")
    elif center_y > frame_center_y + tolerance:
        print("Move camera down")
    else:
        centered_y = True
    
    if((centered_x == True) and (centered_y == True)):
        print("Object is centered")




model = YOLO("yolov8n.pt")
camera_0 = cv2.VideoCapture("http://10.0.0.233:5000/stream")
frames(0)