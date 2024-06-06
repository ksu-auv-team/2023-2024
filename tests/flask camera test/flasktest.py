from flask import Flask, render_template, Response
import cv2 as cv
import numpy as np

from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

app = Flask(__name__)
camera_0 = cv.VideoCapture(0)
camera_1 = cv.VideoCapture(1)

# smallest model of YOLOv8 used for testing
# these models are trained using (mostly) the MS COCO dataset
#change this model in AUV application when model is ready
model = YOLO("yolov8n.pt")

def frames(cnum):  
    while True:
        if cnum == 0:
            success, frame = camera_0.read()
            print("Zed camera:")
        else:
            success, frame = camera_1.read()
            print("Webcam:")
        if not success:
            break
        else:
            center_x , center_y = box_center(frame)
            # 240x320 is half the dimension of the cameras tested
            # adjust these values depending on your cameras resolution
            adjust_camera(center_x, center_y, 240, 320)
            ret, buffer = cv.imencode('.jpg', frame)
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


@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/video_0')
def video_0():
    return Response(frames(0), mimetype='multipart/x-mixed-replace;boundary = frame')

@app.route('/video_1')
def video_1():
    return Response(frames(1), mimetype='multipart/x-mixed-replace;boundary = frame')


if __name__ == "__main__":
    app.run(debug=True)

