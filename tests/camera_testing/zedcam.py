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
    return render_template('index2.html')

@app.route('/video_0')
def video_0():
    try:
        webcam0 = WebCam()
        ip_camera_url_0 = "http://10.0.0.233:5000/stream"  # Replace with your IP camera URL
        return Response(routes.gen_ip(webcam0, ip_camera_url_0), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as err:
        return Response(f'Error {err}')
    
@app.route('/video_1')
def video_1():
    try:
        webcam1 = WebCam()
        ip_camera_url_1 = "http://10.0.0.233:5000/stream"  # Replace with your IP camera URL
        return Response(routes.gen_ip(webcam1, ip_camera_url_1), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as err:
        return Response(f'Error {err}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
