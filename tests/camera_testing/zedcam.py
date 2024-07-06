from flask import Flask, render_template, Response, Blueprint
from controllers import routes
from services.WebCamService import WebCam
import cv2

zedcam_blueprint = Blueprint('zedcam_blueprint', __name__)

zedcam = WebCam(ip="http://10.101.188.170:5000/stream", camera_number=0)


@zedcam_blueprint.route('/video_0')
def video_0():
    try:
        # Replace with your IP camera URL
        webcam0 = WebCam(camera_number=0)
        return Response(routes.gen(webcam0), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as err:
        return Response(f'Error {err}')
