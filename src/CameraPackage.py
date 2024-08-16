from flask import Flask, url_for
from modules.CameraPackageSupport import WebCamService, routes
from modules.CameraPackageSupport.camera_1 import camera_1
from modules.CameraPackageSupport.camera_2 import camera_2

# Creating the custom logger
import logging
logging.basicConfig(
    filename='logs/main.log',      # Name of the log file
    filemode='a',            # Append mode (use 'w' for overwrite each time)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    datefmt='%Y-%m-%d %H:%M:%S',  # Timestamp format
    level=logging.INFO       # Minimum log level to record
)

app = Flask(__name__)
app.register_blueprint(camera_1)
app.register_blueprint(camera_2)
app.register_blueprint(routes.get_blueprint())

#Opening cameras through flask regardless of parameters or configuration
@app.route('/video_0')
def video_0():
    video_url = url_for('camera_1.video_0')
    
    # Make a request to the video_0 endpoint
    response = app.test_client().get(video_url)
    
    # Return the response to the client
    return response.data

@app.route('/video_1')
def video_1():
    video_url = url_for('camera_2.video_1')
    
    # Make a request to the video_0 endpoint
    response = app.test_client().get(video_url)
    
    # Return the response to the client
    return response.data

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5001)