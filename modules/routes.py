from flask import Blueprint, Response, request
from modules.WebCamService import WebCam
import cv2

REQUEST_API = Blueprint('request_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


def gen(webcam):
    capture = cv2.VideoCapture(webcam.camera_number)
    if not capture:
        raise Exception("Error accessing the WebCam")

    while True:
        frame = webcam.get_frame(capture)
        cropped = crop_frame(frame)
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + cropped + b'\r\n\r\n'
        )

def crop_frame(frame):
        # Get the dimensions of the frame
        height, width, _ = frame.shape

        # Crop the right half of the frame
        cropped_frame = frame[:, width // 2:]
        
        return cropped_frame

@REQUEST_API.route('/stream')
def monitoring():
    try:
        webcam = WebCam()
        return Response(gen(webcam), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as err:
        return Response(f'Error {err}')
