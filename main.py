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

# Import custom packages from the modules folder
from static.modules.Controller_Package import Controller
from static.modules.Hardware_Package import HardwarePackage
from static.modules.Movement_Package import MovementPackage
from static.modules.Neural_Network import NeuralNetworkPackage

# Global storage for camera frames and locks
camera_frames = {"usb": None, "zed": None}
camera_locks = {"usb": threading.Lock(), "zed": threading.Lock()}

app = Flask(__name__)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Create the logging objects for the application and setup logging to a file
logging.basicConfig(filename='app.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def usb_camera_capture_thread(camera_index, camera_frames, camera_locks):
    """
    Captures frames from a USB camera in a separate thread.
    
    @param camera_index Index of the camera to capture frames from.
    @param camera_frames Dictionary to store the captured frames.
    @param camera_locks Dictionary of locks for thread-safe frame updates.
    """
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FPS, 30)  # Set frames per second to 30

    # Set lower resolution for higher framerate
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set frame width to 640 pixels
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set frame height to 480 pixels
    
    if not cap.isOpened():
        print(f"Failed to open camera {camera_index}")
        return
    
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            with camera_locks["usb"]:
                _, buffer = cv2.imencode('.jpg', frame)
                camera_frames["usb"] = buffer.tobytes()
    cap.release()

def zed_camera_capture_thread(camera_frames, camera_locks):
    """
    Captures frames from a ZED camera in a separate thread.
    
    @param camera_frames Dictionary to store the captured frames.
    @param camera_locks Dictionary of locks for thread-safe frame updates.
    """
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
    """
    Generator to yield camera frames for streaming.
    
    @param camera_key Key identifying which camera's frames to yield.
    """
    while True:
        if camera_key in camera_frames and camera_frames[camera_key] is not None:
            with camera_locks[camera_key]:
                frame = camera_frames[camera_key]
                yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Database models and Flask routes are defined here...
# (Excluded for brevity, but follow the same pattern for docstrings and inline comments)

@app.route('/video_feed/<int:camera_index>')
def video_feed(camera_index):
    """
    Route to serve the video feed for the requested camera.
    
    @param camera_index The index of the camera to stream video from.
    """
    return Response(generate_frames(camera_index),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """
    Main page route to display available camera feeds.
    """
    cameras = list(camera_frames.keys())
    return render_template('index.html', cameras=cameras)

def shutdown_handler(signum, frame):
    """
    Handles graceful shutdown on receiving a SIGINT signal.
    
    @param signum Signal number.
    @param frame Current stack frame.
    """
    print("Shutdown signal received")
    # Cleanup resources here
    print("Cleanup completed, exiting application")
    exit(0)

# Register the signal handler for SIGINT
signal.signal(signal.SIGINT, shutdown_handler)

if __name__ == '__main__':
    # Start camera capture threads and run the Flask app
    threading.Thread(target=usb_camera_capture_thread, args=(0, camera_frames, camera_locks), daemon=True).start()
    threading.Thread(target=zed_camera_capture_thread, args=(camera_frames, camera_locks), daemon=True).start()
    
    app.run(debug=True, threaded=True, host='0.0.0.0')
