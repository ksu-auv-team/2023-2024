from flask import Flask, Response, render_template
import cv2
import threading
from time import sleep

app = Flask(__name__)

# Global storage for camera frames and locks
camera_frames = {}
camera_locks = {}

def camera_capture_thread(camera_index):
    """
    Thread function for continuously capturing frames from the specified camera.
    """
    global camera_frames, camera_locks
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    # Ensure camera is opened successfully
    if not cap.isOpened():
        print(f"Failed to open camera {camera_index}")
        return
    
    # Initialize lock for current camera
    camera_locks[camera_index] = threading.Lock()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            sleep(0.1)  # Briefly pause on failure before retrying
            continue
        
        # Store the latest frame with thread-safe access
        with camera_locks[camera_index]:
            _, buffer = cv2.imencode('.jpg', frame)
            camera_frames[camera_index] = buffer.tobytes()

    # Release the camera resource when the loop exits
    cap.release()

def generate_frames(camera_index):
    """
    Generator function to yield frames as HTTP response chunks.
    """
    global camera_frames, camera_locks
    
    while True:
        # Wait for the frame to be available
        if camera_index in camera_frames:
            # Ensure thread-safe access to the frame
            with camera_locks[camera_index]:
                frame = camera_frames[camera_index]
                yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            # Frame not available yet, yield empty data or a placeholder
            sleep(0.1)

@app.route('/video_feed/<int:camera_index>')
def video_feed(camera_index):
    """
    Route to serve the video feed for the requested camera.
    """
    return Response(generate_frames(camera_index),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """
    Main page route to display available camera feeds.
    """
    # Example to display links to available camera feeds
    cameras = list(camera_frames.keys())
    return render_template('index.html', cameras=cameras)

if __name__ == '__main__':
    # Pre-start camera capture threads for known camera indices
    for camera_index in [0, 1]:  # Example for cameras at index 0 and 1
        threading.Thread(target=camera_capture_thread, args=(camera_index,), daemon=True).start()
    
    app.run(debug=True, threaded=True, host='0.0.0.0')
