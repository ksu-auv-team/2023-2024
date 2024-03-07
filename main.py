from flask import Flask, Response, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from time import sleep
import numpy as np
import threading
import logging
import signal
import cv2

# Import custom packages from the modules folder
# from static.modules.Controller_Package import Controller
# from static.modules.Hardware_Package import HardwarePackage
# from static.modules.Movement_Package import MovementPackage
# from static.modules.Neural_Network import NeuralNetworkPackage

app = Flask(__name__)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Create the logging objects for the application and setup logging to a file
logging.basicConfig(filename='app.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Database models
class InputData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    X = db.Column(db.Float, nullable=False)
    Y = db.Column(db.Float, nullable=False)
    Z = db.Column(db.Float, nullable=False)
    Roll = db.Column(db.Float, nullable=False)
    Pitch = db.Column(db.Float, nullable=False)
    Yaw = db.Column(db.Float, nullable=False)
    Claw = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"InputData('{self.id}', '{self.date_posted}', '{self.X}', '{self.Y}', '{self.Z}', '{self.Roll}', '{self.Pitch}', '{self.Yaw}', '{self.Claw}')"

class OutputData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    M1 = db.Column(db.Integer, nullable=False)
    M2 = db.Column(db.Integer, nullable=False)
    M3 = db.Column(db.Integer, nullable=False)
    M4 = db.Column(db.Integer, nullable=False)
    M5 = db.Column(db.Integer, nullable=False)
    M6 = db.Column(db.Integer, nullable=False)
    M7 = db.Column(db.Integer, nullable=False)
    M8 = db.Column(db.Integer, nullable=False)
    Claw = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"OutputData('{self.id}', '{self.date_posted}', '{self.M1}', '{self.M2}', '{self.M3}', '{self.M4}', '{self.M5}', '{self.M6}', '{self.M7}', '{self.M8}', '{self.Claw}')"
    
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    OTemp = db.Column(db.Float, nullable=False)
    TTemp = db.Column(db.Float, nullable=False)
    Depth = db.Column(db.Float, nullable=False)
    Humidity = db.Column(db.Float, nullable=False)
    Pressure = db.Column(db.Float, nullable=False)
    Battery1V = db.Column(db.Float, nullable=False)
    Battery2V = db.Column(db.Float, nullable=False)
    Battery3V = db.Column(db.Float, nullable=False)
    Battery1C = db.Column(db.Float, nullable=False)
    Battery2C = db.Column(db.Float, nullable=False)
    Battery3C = db.Column(db.Float, nullable=False)
    X = db.Column(db.Float, nullable=False)
    Y = db.Column(db.Float, nullable=False)
    Z = db.Column(db.Float, nullable=False)
    Roll = db.Column(db.Float, nullable=False)
    Pitch = db.Column(db.Float, nullable=False)
    Yaw = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"SensorData('{self.id}', '{self.date_posted}', '{self.OTemp}', '{self.TTemp}', '{self.Depth}', '{self.Humidity}', '{self.Pressure}', '{self.Battery1V}', \
                            '{self.Battery2V}', '{self.Battery3V}', '{self.Battery1C}', '{self.Battery2C}', '{self.Battery3C}', '{self.X}', '{self.Y}', '{self.Z}', \
                            '{self.Roll}', '{self.Pitch}', '{self.Yaw}')"

@app.route('/get_input_data')
def get_input_data():
    """
    Route to get the input data from the database.
    """
    input_data = InputData.query.query.order_by(InputData.date_posted.desc()).first()
    return input_data

@app.route('/get_output_data')
def get_output_data():
    """
    Route to get the output data from the database.
    """
    output_data = OutputData.query.query.order_by(OutputData.date_posted.desc()).first()
    return output_data

@app.route('/get_sensor_data')
def get_sensor_data():
    """
    Route to get the sensor data from the database.
    """
    sensor_data = SensorData.query.query.order_by(SensorData.date_posted.desc()).first()
    return sensor_data

@app.route('/post_input_data', methods=['POST'])
def post_input_data():
    """
    Route to post the input data to the database.
    """
    data = request.get_json()
    input_data = InputData(X=data['X'], Y=data['Y'], Z=data['Z'], Roll=data['Roll'], Pitch=data['Pitch'], Yaw=data['Yaw'], Claw=data['Claw'])
    db.session.add(input_data)
    db.session.commit()
    return 'Input data posted successfully'

@app.route('/post_output_data', methods=['POST'])
def post_output_data():
    """
    Route to post the output data to the database.
    """
    data = request.get_json()
    output_data = OutputData(M1=data['M1'], M2=data['M2'], M3=data['M3'], M4=data['M4'], M5=data['M5'], M6=data['M6'], M7=data['M7'], M8=data['M8'], Claw=data['Claw'])
    db.session.add(output_data)
    db.session.commit()
    return 'Output data posted successfully'

@app.route('/post_sensor_data', methods=['POST'])
def post_sensor_data():
    """
    Route to post the sensor data to the database.
    """
    data = request.get_json()
    sensor_data = SensorData(OTemp=data['OTemp'], TTemp=data['TTemp'], Depth=data['Depth'], Humidity=data['Humidity'], Pressure=data['Pressure'], 
                             Battery1V=data['Battery1V'], Battery2V=data['Battery2V'], Battery3V=data['Battery3V'], Battery1C=data['Battery1C'], 
                             Battery2C=data['Battery2C'], Battery3C=data['Battery3C'], X=data['X'], Y=data['Y'], Z=data['Z'], Roll=data['Roll'], 
                             Pitch=data['Pitch'], Yaw=data['Yaw'])
    db.session.add(sensor_data)
    db.session.commit()
    return 'Sensor data posted successfully'

@app.route('/')
def index():
    """
    Main page route to display available camera feeds.
    """
    # # Example to display links to available camera feeds
    # cameras = list(camera_frames.keys())
    # return render_template('index.html', cameras=cameras)
    return render_template('index.html')

def shutdown_handler(signum, frame):
    print("Shutdown signal received")

    # Add additional cleanup steps here

    print("Cleanup completed, exiting application")
    # Exit the program
    exit(0)

# Register the signal handler for SIGINT
signal.signal(signal.SIGINT, shutdown_handler)

if __name__ == '__main__':
    # Register the shutdown handler
    signal.signal(signal.SIGINT, shutdown_handler)

    app.run(debug=True, threaded=True, host='0.0.0.0')
