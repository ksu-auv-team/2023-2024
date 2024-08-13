
#commented out as this camera is currently inactive and leaving as is causes errors
from flask import Flask, render_template, Response, Blueprint
from CameraPackageSupport import routes
from CameraPackageSupport.WebCamService import WebCam

anchor_blueprint = Blueprint('camera_2', __name__)


@anchor_blueprint.route('/video_1')
def video_1():
    try:
        anchor_camera = WebCam(camera_number=2)
        return Response(routes.gen(anchor_camera), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as err:
        return Response(f'Error {err}')