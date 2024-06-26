#zedcam.py
from flask import Flask, render_template, Response
from controllers import routes
from services.WebCamService import WebCam
import cv2


#How to load cameras through just link:
# cameraIP/stream

app = Flask(__name__)
app.register_blueprint(routes.get_blueprint())


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_1')
def video_1():
    try:
        webcam = WebCam()
        ip_camera_url = "http://10.0.0.233:5000/stream"  # Replace with your IP camera URL
        return Response(routes.gen_ip(webcam, ip_camera_url), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as err:
        return Response(f'Error {err}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
