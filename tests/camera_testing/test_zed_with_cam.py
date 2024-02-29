from flask import Flask, Response, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from time import sleep
import pyzed.sl as sl
import numpy as np
import threading
import logging
import signal
import cv2

# Global storage for camera frames and locks
camera_frames = {}
camera_locks = {}

# Global storage for camera frames and locks
camera_frames = {"usb": None, "zed": None}
camera_locks = {"usb": threading.Lock(), "zed": threading.Lock()}

def usb_camera_capture_thread(camera_index, camera_frames, camera_locks):
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FPS, 30)

    # Set lower resolution for higher framerate
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Example: set width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Example: set height
    
    # Ensure camera is opened successfully
    if not cap.isOpened():
        print(f"Failed to open camera {camera_index}")
        return
    
    # Initialize lock for current camera
    camera_locks[camera_index] = threading.Lock()
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            with camera_locks["usb"]:
                _, buffer = cv2.imencode('.jpg', frame)
                camera_frames["usb"] = buffer.tobytes()
    cap.release()


def zed_camera_capture_thread(camera_frames, camera_locks):
    init_params = sl.InitParameters()
    cap = sl.Camera()
    if cap.open(init_params) != sl.ERROR_CODE.SUCCESS:
        print("Failed to open ZED camera")
        return
    
    image = sl.Mat()
    runtime_parameters = sl.RuntimeParameters()
    
    while cap.is_opened():
        if cap.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            cap.retrieve_image(image, sl.VIEW.LEFT)
            frame = image.get_data()
            with camera_locks["zed"]:
                _, buffer = cv2.imencode('.jpg', frame)
                camera_frames["zed"] = buffer.tobytes()
    cap.close()

def generate_frames(camera_key):
    while True:
        if camera_key in camera_frames and camera_frames[camera_key] is not None:
            with camera_locks[camera_key]:
                frame = camera_frames[camera_key]
                yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed/<int:camera_index>')
def video_feed(camera_index):
    """
    Route to serve the video feed for the requested camera.
    """
    return Response(generate_frames(camera_index),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
