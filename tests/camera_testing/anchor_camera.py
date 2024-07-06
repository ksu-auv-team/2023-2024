
#commented out as this camera is currently inactive and leaving as is causes errors
from flask import Flask, render_template, Response, Blueprint
from controllers import routes
from services.WebCamService import WebCam
import cv2

anchor_blueprint = Blueprint('anchor_blueprint', __name__)


@anchor_blueprint.route('/video_1')
def video_1():
    try:
        anchor_camera = WebCam(camera_number=1)
        return Response(routes.gen(anchor_camera), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as err:
        return Response(f'Error {err}')


