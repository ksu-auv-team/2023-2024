"""
    Main file for the project.
    For now this script handles the backend subprocesses of the project.
    Four sub-processes are handles:
        - Hardware Interface
        - Movement Package
        - Neural Network Package
        - Web Interface

    These four sub-processes will be run in parallel to each other and communicate via the custom database system.

    The main script will be responsible for handling the communication between the sub-processes and the handling of the state machine.
    The state machine will be responsible for the overall control of the project.
"""

# Importing the necessary libraries
from flask import Flask, request, jsonify, render_template, send_from_directory, Blueprint, url_for
from flask_sqlalchemy import SQLAlchemy
import subprocess
import argparse
import time
import sys
import os
from modules import WebCamService, routes
from modules.zedcam import zedcam_blueprint
from modules.anchor_camera import anchor_blueprint

# Creating the custom logger
import logging
logging.basicConfig(
    filename='logs/main.log',      # Name of the log file
    filemode='a',            # Append mode (use 'w' for overwrite each time)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    datefmt='%Y-%m-%d %H:%M:%S',  # Timestamp format
    level=logging.INFO       # Minimum log level to record
)

# Creating the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///KSUAUV.db'  # Adjust for your database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Set the upload folder relative to the current script's directory
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

app.register_blueprint(routes.get_blueprint())
app.register_blueprint(zedcam_blueprint)
app.register_blueprint(anchor_blueprint)

class SubprocessHandler:
    def __init__(self, command):
        self.command = command
        self.process = None

    def start(self):
        if self.process is None:
            self.process = subprocess.Popen(self.command)
            print(f"Started subprocess with PID: {self.process.pid}")
        else:
            print("Process is already running.")

    def stop(self):
        if self.process is not None:
            self.process.terminate()  # Graceful termination
            self.process.wait()  # Wait for the process to terminate
            print(f"Terminated subprocess with PID: {self.process.pid}")
            self.process = None
        else:
            print("Process is not running.")
            
commands = [
    [['HIT'], ["python3", "modules/HardwareInterface.py", "--T"]], # Runs the hardware interface in test mode and give it the name HIT
    [['HIR'], ["python3", "modules/HardwareInterface.py", "--R"]], # Runs the hardware interface normally and give it the name HIR
    [['MIT'], ["python3", "modules/MovementPackage.py", "--T"]], # Runs the movement package in test mode and give it the name MIT
    [['MIR'], ["python3", "modules/MovementPackage.py", "--R"]], # Runs the movement package normally and give it the name MIR
    [['NIT'], ["python3", "modules/NeuralNetwork.py", "--T"]], # Runs the neural network package in test mode and give it the name NIT
    [['NIR'], ["python3", "modules/NeuralNetwork.py", "--R"]], # Runs the neural network package normally and give it the name NIR
]

subprocesses = {f'{command[0]}: {SubprocessHandler(command[1])}' for command in commands}

class Sensors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voltage1 = db.Column(db.Float, nullable=True)
    voltage2 = db.Column(db.Float, nullable=True)
    voltage3 = db.Column(db.Float, nullable=True)
    current1 = db.Column(db.Float, nullable=True)
    current2 = db.Column(db.Float, nullable=True)
    current3 = db.Column(db.Float, nullable=True)
    error = db.Column(db.Integer, nullable=True)
    depth = db.Column(db.Float, nullable=True)
    X = db.Column(db.Float, nullable=True)
    Y = db.Column(db.Float, nullable=True)
    Z = db.Column(db.Float, nullable=True)
    pitch = db.Column(db.Float, nullable=True)
    roll = db.Column(db.Float, nullable=True)
    yaw = db.Column(db.Float, nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    orin_temp = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    heading = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        return f'<{self.id}, {self.voltage1}, {self.voltage2}, \
                  {self.volage3}, {self.current1}, {self.current2}, \
                  {self.current3}, {self.depth}, {self.X}, \
                  {self.Y}, {self.Z}, {self.pitch}, \
                  {self.roll}, {self.yaw}, {self.temperature}, \
                  {self.orin_temp}, {self.humidity}, {self.heading}>'

class Output(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    M1 = db.Column(db.Integer, nullable=False)
    M2 = db.Column(db.Integer, nullable=False)
    M3 = db.Column(db.Integer, nullable=False)
    M4 = db.Column(db.Integer, nullable=False)
    M5 = db.Column(db.Integer, nullable=False)
    M6 = db.Column(db.Integer, nullable=False)
    M7 = db.Column(db.Integer, nullable=False)
    M8 = db.Column(db.Integer, nullable=False)
    Claw = db.Column(db.Integer, nullable=False)
    Torp1 = db.Column(db.Boolean, nullable=False)
    Torp2 = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<{self.id}, {self.M1}, {self.M2}, \
                  {self.M3}, {self.M4}, {self.M5}, \
                  {self.M6}, {self.M7}, {self.M8}, \
                  {self.Claw}, {self.Torp1}, {self.Torp2}>'

class Input(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    X = db.Column(db.Float, nullable=False)
    Y = db.Column(db.Float, nullable=False)
    Z = db.Column(db.Float, nullable=False)
    pitch = db.Column(db.Float, nullable=False)
    roll = db.Column(db.Float, nullable=False)
    yaw = db.Column(db.Float, nullable=False)
    claw = db.Column(db.Integer, nullable=False)
    torp1 = db.Column(db.Boolean, nullable=False)
    torp2 = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<{self.id}, {self.X}, {self.Y}, \
                  {self.Z}, {self.pitch}, {self.roll}, \
                  {self.yaw}, {self.claw}, {self.torp1}, \
                  {self.torp2}>'
                  
class Objects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    angle = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<{self.id}, {self.object}, {self.distance}, {self.angle}>'

# Creating the flask routes to handle the data
@app.route('/sensors', methods=['POST'])
def add_sensor_data():
    data = request.get_json()

    new_sensor_data = Sensors(voltage1=data['voltage1'], voltage2=data['voltage2'], voltage3=data['voltage3'],
                              current1=data['current1'], current2=data['current2'], current3=data['current3'],
                              depth=data['depth'], X=data['X'], Y=data['Y'], Z=data['Z'],
                              pitch=data['pitch'], roll=data['roll'], yaw=data['yaw'],
                              temperature=data['temperature'], orin_temp=data['orin_temp'], humidity=data['humidity'],
                              heading=data['heading'])

    db.session.add(new_sensor_data)
    db.session.commit()

    return 'Data added', 201

@app.route('/sensors', methods=['GET'])
def get_sensor_data():
    sensor_data = Sensors.query.order_by(Sensors.id.desc()).first()
    if sensor_data:
        data_dict = {
            'voltage1': sensor_data.voltage1, 'voltage2': sensor_data.voltage2, 'voltage3': sensor_data.voltage3,
            'current1': sensor_data.current1, 'current2': sensor_data.current2, 'current3': sensor_data.current3,
            'depth': sensor_data.depth, 'X': sensor_data.X, 'Y': sensor_data.Y, 'Z': sensor_data.Z,
            'pitch': sensor_data.pitch, 'roll': sensor_data.roll, 'yaw': sensor_data.yaw,
            'temperature': sensor_data.temperature, 'orin_temp': sensor_data.orin_temp, 'humidity': sensor_data.humidity,
            'heading': sensor_data.heading
        }
        return jsonify(data_dict)
    else:
        return jsonify({'message': 'No data found'}), 404

@app.route('/output', methods=['POST'])
def add_output_data():
    data = request.get_json()

    new_output_data = Output(M1=data['M1'], M2=data['M2'], M3=data['M3'], M4=data['M4'],
                             M5=data['M5'], M6=data['M6'], M7=data['M7'], M8=data['M8'],
                             Claw=data['Claw'], Torp1=data['Torp1'], Torp2=data['Torp2'])

    db.session.add(new_output_data)
    db.session.commit()

    return 'Data added', 201

@app.route('/output', methods=['GET'])
def get_output_data():
    output_data = Output.query.order_by(Output.id.desc()).first()
    if output_data:
        data_dict = {
            'M1': output_data.M1, 'M2': output_data.M2, 'M3': output_data.M3, 'M4': output_data.M4,
            'M5': output_data.M5, 'M6': output_data.M6, 'M7': output_data.M7, 'M8': output_data.M8,
            'Claw': output_data.Claw, 'Torp1': output_data.Torp1, 'Torp2': output_data.Torp2
        }
        return jsonify(data_dict)
    else:
        return jsonify({'message': 'No data found'}), 404

@app.route('/input', methods=['POST'])
def add_input_data():
    data = request.get_json()

    new_input_data = Input(X=data['X'], Y=data['Y'], Z=data['Z'],
                           pitch=data['Pitch'], roll=data['Roll'], yaw=data['Yaw'],
                           claw=data['Claw'], torp1=data['Torpedo_1'], torp2=data['Torpedo_2'])

    db.session.add(new_input_data)
    db.session.commit()
    # print(new_input_data)

    return 'Data added', 201

@app.route('/input', methods=['GET'])
def get_input_data():
    input_data = Input.query.order_by(Input.id.desc()).first()
    if input_data:
        data_dict = {
            'X': input_data.X, 'Y': input_data.Y, 'Z': input_data.Z,
            'pitch': input_data.pitch, 'roll': input_data.roll, 'yaw': input_data.yaw,
            'claw': input_data.claw, 'torp1': input_data.torp1, 'torp2': input_data.torp2
        }
        # print(data_dict)
        return jsonify(data_dict)
    else:
        return jsonify({'message': 'No data found'}), 404

@app.route('/objects', methods=['POST'])
def add_object_data():
    data = request.get_json()

    new_object_data = Objects(object=data['object'], distance=data['distance'], angle=data['angle'])

    db.session.add(new_object_data)
    db.session.commit()

    return 'Data added', 201

@app.route('/objects', methods=['GET'])
def get_object_data():
    object_data = Objects.query.order_by(Objects.id.desc()).first()
    if object_data:
        data_dict = {
            'object': object_data.object, 
            'distance': object_data.distance, 
            'angle': object_data.angle
        }
        return jsonify(data_dict)
    else:
        return jsonify({'message': 'No data found'}), 404

#Opening cameras through flask regardless of parameters or configuration
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

# Create the Hardware Interface routes
@app.route('/run_hardware_interface', methods=['POST'])
def run_hardware_interface():
    subprocesses['HIR'].start()
    return 'Hardware Interface Running', 201

@app.route('/run_hardware_interface_test', methods=['POST'])
def run_hardware_interface_test():
    subprocesses['HIT'].start()
    return 'Hardware Interface Test Running', 201

@app.route('/stop_hardware_interface', methods=['POST'])
def stop_hardware_interface():
    subprocesses['HIR'].stop()
    subprocesses['HIT'].stop()
    return 'Hardware Interface Stopped', 201

@app.route('/run_movement_package', methods=['POST'])
def run_movement_package():
    subprocesses['MIR'].start()
    return 'Movement Package Running', 201

@app.route('/run_movement_package_test', methods=['POST'])
def run_movement_package_test():
    subprocesses['MIT'].start()
    return 'Movement Package Test Running', 201

@app.route('/stop_movement_package', methods=['POST'])
def stop_movement_package():
    subprocesses['MIR'].stop()
    subprocesses['MIT'].stop()
    return 'Movement Package Stopped', 201

@app.route('/run_neural_network', methods=['POST'])
def run_neural_network():
    subprocesses['NIR'].start()
    return 'Neural Network Running', 201

@app.route('/run_neural_network_test', methods=['POST'])
def run_neural_network_test():
    subprocesses['NIT'].start()
    return 'Neural Network Test Running', 201

@app.route('/stop_neural_network', methods=['POST'])
def stop_neural_network():
    subprocesses['NIR'].stop()
    subprocesses['NIT'].stop()
    return 'Neural Network Stopped', 201

@app.route('/run_all', methods=['POST'])
def run_all():
    subprocesses['HIR'].start()
    subprocesses['MIR'].start()
    subprocesses['NIR'].start()
    return 'All Subprocesses Running', 201

@app.route('/run_all_test', methods=['POST'])
def run_all_test():
    subprocesses['HIT'].start()
    subprocesses['MIT'].start()
    subprocesses['NIT'].start()
    return 'All Subprocesses Running in Test Mode', 201

@app.route('/stop_all', methods=['POST'])
def stop_all():
    subprocesses['HIR'].stop()
    subprocesses['MIR'].stop()
    subprocesses['NIR'].stop()
    subprocesses['HIT'].stop()
    subprocesses['MIT'].stop()
    subprocesses['NIT'].stop()
    return 'All Subprocesses Stopped', 201

@app.route('/shutdown', methods=['POST'])
def shutdown():
    stop_all()
    time.sleep(1)
    sys.exit()

@app.route('/')
def index():
    return render_template('index.html')

def create_tables():
    db.create_all()

def main(ip : str = "192.168.0.106"):
    with app.app_context():
        create_tables()
    
    app.run(debug=True, host=ip, port=5000)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Main script for the KSUAUV project.')
    parser.add_argument('--ip', type=str, default='192.168.0.106', help='The IP address to run the server on.')
    args = parser.parse_args()
    main(args.ip)