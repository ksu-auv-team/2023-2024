from flask import Flask, render_template, Response, url_for
from controllers import routes
from services.WebCamService import WebCam
import cv2
from anchor_camera import anchor_blueprint
from zedcam import zedcam_blueprint

app = Flask(__name__)
app.register_blueprint(routes.get_blueprint())
app.register_blueprint(zedcam_blueprint)
app.register_blueprint(anchor_blueprint)


@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/video_0')
def video_0():
    video_url = url_for('zedcam_blueprint.video_0')
    
    # Make a request to the video_0 endpoint
    response = app.test_client().get(video_url)
    
    # Return the response to the client
    return response.data

@app.route('/video_1')
def video_1():
    video_url = url_for('anchor_blueprint.video1')
    
    # Make a request to the video_0 endpoint
    response = app.test_client().get(video_url)
    
    # Return the response to the client
    return response.data


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)