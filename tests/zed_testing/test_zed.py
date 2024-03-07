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
    """
    Route to stream video from a regular webcam.
    Captures video from the default camera (usually the first webcam found on the system).
    Streams the captured video as a JPEG image.
    """
    cap = cv2.VideoCapture(2)  # Make sure the device index is correct for your setup
    if not cap.isOpened():
        print("Error: Could not open video device. Please check the device index and permissions.")
        return Response("Error: Could not open video device.", status=500)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Warning: Empty frame read from camera. Skipping.")
                continue  # Skip this iteration and try reading the next frame
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error: Frame could not be encoded. Skipping.")
                continue
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    finally:
        cap.release()  # Make sure to release the camera


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')