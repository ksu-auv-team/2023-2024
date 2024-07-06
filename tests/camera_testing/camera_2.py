'''from flask import Flask, render_template, Response, Blueprint
from controllers import routes
from services.WebCamService import WebCam
import cv2

camera2_blueprint = Blueprint('camera2_blueprint', __name__)

camera2 = WebCam(camera_number=1)


@camera2_blueprint.route('/video_1')
def video_1():
    try:
        anchor_camera = WebCam(camera_number=1)
        #ip_camera_url_1 = "http://10.0.0.233:5000/stream"  # Replace with your IP camera URL
        return Response(routes.gen(camera2), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as err:
        return Response(f'Error {err}')
'''

