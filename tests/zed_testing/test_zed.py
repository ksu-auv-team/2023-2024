import pyzed.sl as sl
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

@app.route('/zed_stream')
def zed_stream():
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD720
    init.depth_mode = sl.DEPTH_MODE.PERFORMANCE
    init.coordinate_units = sl.UNIT.METER
    zed = sl.Camera()
    status = zed.open(init)
    runtime = sl.RuntimeParameters()
    mat = sl.Mat()
    while True:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(mat, sl.VIEW.LEFT)
            image = mat.get_data()
            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            
# Create a route to stream a regular camera stream
@app.route('/cam_stream')
def cam_stream():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)